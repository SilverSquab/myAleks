from .models import *
import datetime
from jinja2 import *
import pymongo
import json
from webapps.quiz.models import Question, Option
from bisect import bisect_right

def tuple_insort(tuple_list, t):
    keys = [t[1] for t in tuple_list]
    i = bisect_right(keys, t[1])
    tuple_list.insert(i, t)

# return file name and dir
'''
def generate_pdf(quiz_id, template_name=''):
    if template_name == '':
        template_name = 'standard.tex'
    env = Environment(loader=PackageLoader('webapps.quiz', 'pdftemplates'))
    try:
        template = env.get_template(template_name)
    except:
        raise Exception('template doesn\'t exist')

    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except:
        raise Exception('quiz does not exist')

    #TODO: here is only body, other info should also be here.
    question_dic = json.loads(quiz.body)
    questions = []
    for qid in question_dic:
        try:
            question = Question.objects.get(id = qid)
            questions.append(question)
        except:
            continue
    
    print(template.render(questions=questions))
'''

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

'''
mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)

def log_question_record(question_id, option_id, option_order, is_correct, student_id):
    collection = mongo_client.student_log.question_records
    data = {
        'question_id': question_id,
        'option_id': option_id,
        'is_correct': is_correct,
        'student_id': student_id,
        'option_order': option_order,
        'datetime': datetime.datetime.utcnow(),
    }

    collection.insert_one(data)
    return True
'''

# convert answers to belief score
# {question_id: order} -> {knowledge_node_id: score}

def answers_to_nodes(answer_dic):
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

        # {node_id: {correct: xx, count: xx}}
        
        for node in question.knowledge_node.all():
            if node.id in nodes_dic:
                nodes_dic[node.id]['count'] += 1
            else:
                nodes_dic[node.id] = {'count': 1, 'correct': 0}
            
            if is_correct:
                nodes_dic[node.id]['correct'] += 1
            else:
                pass
            #if nodes_dic[node.id] >= 3:
            #    nodes_dic[node.id] = 3
            #elif nodes_dic[node.id] <= -3:
            #    nodes_dic[node.id] = -3

    node_score_dic = {}
    for node_id in nodes_dic:
        node_score_dic[node_id] = nodes_dic[node_id]['correct'] / float(nodes_dic[node_id]['count'])
                
    return {'status': True, 'data': node_score_dic, 'nodes_dic': nodes_dic}

# get error reasons, create student quiz record, update quiz record
def mark_quiz_wrapper(student_id, quiz_record_id, answer_dic):
    #TODO: create student quiz record
    # TODO: update quiz record
    student_id = str(student_id)

    try:
        sqr = StudentQuizRecord(student=student_id, quiz_record=quiz_record_id)
    except:
        return {'status': False, 'reason': 'student quiz record cannot be created'}

    try:
        quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
    except:
        return {'status': False, 'reason': 'quiz record not existed'}
    
    quiz = quiz_record.quiz

    # count score
    total_score = 0
    body = json.loads(quiz.body)
    qid_score_dic = {}
    for order in body:
        question_id = body['order'][0]
        score = body['order'][1]
        qid_score_dic[question_id] = score

    data = {}
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
            total_score += qid_score_dic.get(question_id, 0)

        else:
            error_reasons += option.error_reason.all().values_list('description', flat=True)



    error_reasons = list(set(error_reasons))

    data['error_reasons'] = error_reasons
    data['total_score'] = total_score
    sqr.score = total_score
    sqr.stats = answer_dic
    sqr.save()

    try:
        info = json.loads(quiz.info)
        participants = info.get('participants', [])
        non_participants = info.get('non_participants', [])
        t = (student_id, total_score)
        tuple_insort(participants, t)
        if student_id in non_participants:
            non_participants.remove(student_id)
        quiz.info = json.dumps({'non_participants': non_participants, 'participants': participants})

    except:
        return {'status': False, 'reason': 'quiz info not correct'}

    return data
