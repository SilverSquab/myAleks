from .models import *
import datetime
from jinja2 import *
import pymongo
import json
from .models import Question, Option

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


def adjust_student_vector(question_id, option, student_id):
    #TODO: adjust a student's knowledge vector after marking a question.
    # may have different implementation using different algos
    pass

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


# convert answers to belief score
# {question_id: order} -> {knowledge_node_id: score}
def mark_quiz(request_dic):
    nodes_dic = {}
    answer_dic = request_dic['questionAndAnswer']
    for question_id in answer_dic:
        try:
            question = Question.objects.get(pk=question_id)
        except:
            return (False, "query question failed")

        try:
            #option = Option.objects.get(pk=option_id)
            option = question.options.get(order = answer_dic[question_id])
        except:
            print(question_id)
            continue
            return (False, "query option faield")

        if option.question != question:
            return (False, "option not belonged to this question")
        
        is_correct = option.is_correct

        for node in question.knowledge_node.all():
            if is_correct:
                score = 1
            else:
                score = -1

            if node.id in nodes_dic:
                nodes_dic[node.id] += score
            else:
                nodes_dic[node.id] = score
            
            if nodes_dic[node.id] >= 3:
                nodes_dic[node.id] = 3
            elif nodes_dic[node.id] <= -3:
                nodes_dic[node.id] = -3
                
    return nodes_dic

