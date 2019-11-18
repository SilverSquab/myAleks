from .models import *
import datetime
from jinja2 import *
import pymongo
import json
from webapps.quiz.models import Question, Option
from bisect import bisect_right
from webapps.student.models import StudentQuizRecord, StudentProfile

def tuple_insort(tuple_list, t):
    keys = [t[1] for t in tuple_list]
    i = bisect_right(keys, t[1])
    tuple_list.insert(i, t)



def mark_question(question_id, option_id, student_id):
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return (False, "query question faield")

    try:
        option = Option.objects.get(pk=option_id)
    except:
        return (False, "query option faield")

    if option.question != question:
        return (False, "option not belonged to this question")

    is_correct = option.is_correct
    if option.order:
        option_order = option.order
    else:
        option_order = 'NA'

    # Log student question record
    log_question_record(
        question_id = question_id,
        option_id = option_id,
        option_order = option_order,
        is_correct = is_correct,
        student_id = student_id,
    )
    
    # update student ks vector
    for node in question.knowledge_node.all():
        update_node(student_id, node.id, 1.0, (1 if is_correct else 0), True, is_correct)

    # TODO: update question stat

# convert answers to belief score
# {question_id: order} -> {knowledge_node_id: score}

def answers_to_nodes(answer_dic):
    # {node_id: {correct: xx, count: xx}}
    nodes_dic = {}
    for question_id in answer_dic:
        try:
            question = Question.objects.get(pk=question_id)
        except:
            return {'status': False, 'reason': "question not existed"}

        try:
            #option = Option.objects.get(pk=option_id)
            option = question.options.get(order = answer_dic[question_id])
        except:
            return {'status': False, 'reason': "option not existed"}

        if option.question != question:
            return {'status': False, 'reason': "option not belong to this question"}
        
        is_correct = option.is_correct

        
        for node in question.knowledge_node.all():
            if node.id in nodes_dic:
                nodes_dic[node.id]['count'] += 1
            else:
                nodes_dic[node.id] = {'count': 1, 'correct': 0}
            
            if is_correct:
                nodes_dic[node.id]['correct'] += 1
            else:
                pass


        for node in option.knowledge_node.all():
            if node.id in nodes_dic:
                nodes_dic[node.id]['count'] += 1
            else:
                nodes_dic[node.id] = {'count': 1, 'correct': 0}
            
            if is_correct:
                nodes_dic[node.id]['correct'] += 1
            else:
                pass

    node_score_dic = {}
    for node_id in nodes_dic:
        node_score_dic[node_id] = nodes_dic[node_id]['correct'] / float(nodes_dic[node_id]['count'])
                
    return {'status': True, 'data': node_score_dic, 'nodes_dic': nodes_dic}

# get error reasons, create student quiz record, update quiz record
def mark_quiz_wrapper(student_id, quiz_record_id, answer_dic):
    student_id = str(student_id)

    try:
        quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
    except:
        return {'status': False, 'reason': 'quiz record not existed'}

    try:
        p = StudentProfile.objects.get(student_no=student_id)
    except:
        return {'status': False, 'reason': 'student profile not existed'}

    if StudentQuizRecord.objects.filter(student=p, quiz_record=quiz_record).exists():
        return {'status': False, 'reason': 'student already taken this quiz'}

    try:
        sqr = StudentQuizRecord.objects.create(student=p, quiz_record=quiz_record)
    except:
        return {'status': False, 'reason': 'student quiz record cannot be created'}


    quiz = quiz_record.quiz

    # count score
    total_score = 0
    body = json.loads(quiz.body)
    qid_score_dic = {}
    for order in body:
        question_id = body[order][0]
        score = body[order][1]
        qid_score_dic[question_id] = score

    question_num = len(body)

    data = {}

    # count error reasons
    error_reasons = []
    for question_id in answer_dic:
        try:
            question = Question.objects.get(pk=question_id)
        except:
            return {'status': False, 'reason': 'question not existed'}

        try:
            option = question.options.get(order = answer_dic[question_id])
        except:
            return {'status': False, 'reason': 'option not existed'}

        if option.question != question:
            return {'status': False, 'reason': 'option not belong to this question'}

        is_correct = option.is_correct
        if is_correct:
            score = qid_score_dic.get(question_id, 0)
            if score == 0:
                score = 1.0 / question_num
            total_score += score
        else:
            #total_score += 1.0 / question_num
            error_reasons += option.error_reason.all().values_list('description', flat=True)



    error_reasons = list(set(error_reasons))

    total_score = round(total_score, 2)
    data['error_reasons'] = error_reasons
    data['total_score'] = total_score
    sqr.score = total_score
    sqr.stats = json.dumps(answer_dic)
    sqr.save()

    #update highest, lowest and average

    # try:
    info = json.loads(quiz_record.info)
    participants = info.get('participants', [])
    non_participants = info.get('non_participants', [])
    t = (student_id, total_score)
    tuple_insort(participants, t)
    if student_id in non_participants:
        non_participants.remove(student_id)

    if "highest_score" in info:
        if total_score >= info['highest_score']:
            info['highest_score'] = round(total_score, 2)
    else:
        info['highest_score'] = round(total_score, 2)

    if 'lowest_score' in info:
        if total_score <= info['lowest_score']:
            info['lowest_score'] = round(total_score, 2)
    else:
        info['lowest_score'] = round(total_score, 2)

    #compute average score
    info['average_score'] = round(sum([t[1] for t in participants])  / len(participants), 2)

    info['participants'] = participants
    info['non_participants'] = non_participants

    #print(info)

    quiz_record.info = json.dumps(info)
    quiz_record.save()

    stats = json.loads(quiz_record.stats)
    try:        
        for qid in answer_dic:
            answer_order = answer_dic[qid]
            if qid in stats:
                if answer_order in stats[qid]:
                    stats[qid][answer_order] += 1
                else:
                    stats[qid][answer_order] = 1

            else:
                stats[qid] = {"A":0, "B":0, "C":0, "D":0}
                if answer_order in stats[qid]:
                    stats[qid][answer_order] += 1
                else:
                    stats[qid][answer_order] = 1

        quiz_record.stats = json.dumps(stats)
        quiz_record.save()
    except:
        return {'status': False, 'reason': 'quiz info not correct'}

    data['status'] = True
    return data

def answer_dic_to_answer_sheet(answer_dic, body):
    res = {}
    for key in body:
        if key in answer_dic:
            res[key] = answer_dic[key]
    return res


def class_answers_to_nodes(answer_dic):
    # {node_id: {correct: xx, count: xx}}
    nodes_dic = {}
    node_question_dic = {}
    correct_count = {}
    for question_id in answer_dic:
        try:
            question = Question.objects.get(pk=question_id)
        except:
            return {'status': False, 'reason': "question not existed"}

        correct_count[question_id] = {'correct': 0, 'count': 0}
        nodes = question.knowledge_node.all()

        for node in nodes:
            if node.id in node_question_dic:
                node_question_dic[node.id].append(question_id)
            else:
                node_question_dic[node.id] = [question_id]

        for order in answer_dic[question_id]:
            try:
                #option = Option.objects.get(pk=option_id)
                option = question.options.get(order = order)
            except:
                return {'status': False, 'reason': "option not existed"}

            if option.question != question:
                return {'status': False, 'reason': "option not belong to this question"}
            
            is_correct = option.is_correct

            times = answer_dic[question_id][order]

            if times == 0:
                continue


            if is_correct:
                correct_count[question_id]['correct'] = times
            correct_count[question_id]['count'] += times

            nodes = option.knowledge_node.all()

            for node in question.knowledge_node.all():
                if node.id in nodes_dic:
                    nodes_dic[node.id]['count'] += times
                else:
                    nodes_dic[node.id] = {'count': times, 'correct': 0}
                
                if is_correct:
                    nodes_dic[node.id]['correct'] += times
                else:
                    pass


            for node in option.knowledge_node.all():
                if node.id in nodes_dic:
                    nodes_dic[node.id]['count'] += times
                else:
                    nodes_dic[node.id] = {'count': times, 'correct': 0}
                
                if is_correct:
                    nodes_dic[node.id]['correct'] += times
                else:
                    pass

    node_score_dic = {}
    for node_id in nodes_dic:
        node_score_dic[node_id] = round(nodes_dic[node_id]['correct'] / float(nodes_dic[node_id]['count']), 1)
    
    return {'status': True, 'node_score_dic': node_score_dic, 'nodes_dic': nodes_dic, 'node_question_dic': node_question_dic, 'correct_count': correct_count}
