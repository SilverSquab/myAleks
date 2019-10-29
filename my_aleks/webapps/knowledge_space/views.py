from .batch_input import *
from functools import reduce
from webapps.school.models import *
from webapps.textbook.models import *
from .student_vector import *
from django.views.decorators.csrf import csrf_exempt

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from webapps.quiz.models import Question,Option
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


@staff_member_required
def upload_knowledge_nodes(request):
    if request.method == 'GET':
        return render(request, 'knowledge_space/upload_knowledge_nodes.html')
        
    f = request.FILES.get('nodes', None)
    #print(f.name)
    #print(f.size)
    if f == None:
        # TODO
        return render(request, 'knowledge_space/upload_knowledge_nodes.html')
    #print(1)
    read_knowledge_nodes_from_file(f) 
    return HttpResponse('OK')

@csrf_exempt
@login_required
def ajax_delete_edge_question(request):
    question_id=request.GET.get("question_id",'')
    edge_id=request.GET.get("edge_id","")
    option_order=request.GET.get("option_order","")
    question_id=int(question_id)
    if option_order:
        question=Question.objects.get(pk=question_id)
        option = Option.objects.get(question=question,order=option_order)
        option.knowledge_node.remove(edge_id)
        return HttpResponse('OK')
    try:
        question=Question.objects.get(pk=question_id)
    except:
        return HttpResponse('question does not exist')
    question.knowledge_node.remove(edge_id)
    return HttpResponse('OK')


@login_required
def upload_knowledge_edges(request):
    if request.method == 'GET':
        return render(request, 'knowledge_space/upload_knowledge_edges.html')
        
    f = request.FILES.get('edges', None)
    #print(f.name)
    #print(f.size)
    if f == None:
        # TODO
        return render(request, 'knowledge_space/upload_knowledge_edges.html')
    #print(1)
    read_knowledge_edges_from_file(f) 
    return HttpResponse('OK')

@login_required
def ajax_nodes(request):
    text = request.GET.get('text', '')
    subject = request.GET.get('subject', '')
    if subject == '':
        nodes = KnowledgeNode.objects.filter(description__contains=text)
        #print(nodes)

    else:
        nodes = KnowledgeNode.objects.filter(graph__subject=subject, description__contains=text)
    nodes_info = nodes.values_list('id', 'description')
    nodes_info = list(nodes_info)
    return HttpResponse(json.dumps(nodes_info))

@csrf_exempt
@login_required
def get_node_chineseName(request):
    if request.method == 'GET':
        return HttpResponse(status=400)
    node_list = json.loads(request.body.decode('utf-8'))
    for index in node_list:
        #print(index)
        try:
            index["chinese_name"]=KnowledgeNode.objects.get(pk=index['name']).title
        except:
            return HttpResponse("node does not exist")
    return HttpResponse(json.dumps(node_list))

@csrf_exempt
@login_required
def ajax_upload_edge(request):
    if request.method == 'GET':
        return HttpResponse(status=400)

    print(request.POST)
    node1_id = request.POST.get('node1_id', '')
    node2_id = request.POST.get('node2_id', '')
    weight = request.POST.get('weight', '1')
    weight = float(weight)
    try:
        node1 = KnowledgeNode.objects.get(pk = node1_id)
        node2 = KnowledgeNode.objects.get(pk = node2_id)
    except:
        return HttpResponse('node does not exist')

    e = KnowledgeGraphEdge.objects.get_or_create(predecessor=node1, successor=node2)[0]
    e.weight = weight
    e.save()

    return HttpResponse('OK')


@staff_member_required
def upload_edge(request):
    if request.method == 'GET':
        #question_form = QuestionForm()
        #option_form = OptionForm()
        return render(request, 'knowledge_space/upload_edge.html', locals())

    else:
        
        #for k in request.POST:
        #    print(k, request.POST[k])
        
        #question_form = QuestionForm()
        #option_form = OptionForm()
        return render(request, 'knowledge_space/upload_edge.html', locals())
    
@login_required
def ajax_subjects(request):
    subjects = Subject.objects.all()
    subjects_info = subjects.values_list('name', 'chinese_name')
    return HttpResponse(json.dumps(list(subjects_info)))


def get_student_graph_vector(request):
    if request.method != 'GET':
        return HttpResponse('failed: method should be get')

    student_id = request.GET.get('student_id', '')
    graph_id = request.GET.get('graph_id', '')

    if not student_id:
        return HttpResponse('failed: student id missing')

    if not graph_id:
        return HttpResponse('failed: graph id missing')
    student_no = StudentProfile.objects.get(pk=student_id).student_no    
    result = json.loads(get_or_create_graph_vector(student_no, graph_id))
    if result['status'] == 'fail':
        return HttpResponse('failed: ' + result['reason'])

    return HttpResponse(json.dumps(result['data']))


def get_student_section_vector(request):
    if request.method != 'GET':
        return HttpResponse('failed: method should be get')

    student_id = request.GET.get('student_id', '')
    section_id = request.GET.get('section_id', '')
    student_no = StudentProfile.objects.get(pk=student_id).student_no

    return HttpResponse(get_student_section_vector_wrapper(student_no, section_id))


def get_student_section_vector_wrapper(student_id, section_id):
    try:
        section = Section.objects.get(pk=section_id)
    except:
        return 'failed: section not existed'

    nodes_list = KnowledgeNode.objects.filter(pk__in=json.loads(section.nodes_list))

    graph_list = list(set(map(lambda x: x.graph, nodes_list)))

    result = {}
    for graph in graph_list:
        tmp = json.loads(get_or_create_graph_vector(student_id, graph.pk))
        if tmp['status'] == 'fail':
            return 'failed: ' + tmp['reason']

        d = tmp['data'].copy()
        nl = json.loads(section.nodes_list)
        for key in tmp['data']:
            if key not in nl:
                d.pop(key)

        result[graph.pk] = d

    return json.dumps(result)
    

def get_student_chapter_vector_wrapper(student_id, chapter_id):
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
    except:
        return 'failed: chapter not existed'

    sections = chapter.sections.all()
    
    result = {}

    for section in sections:
        r = get_student_section_vector_wrapper(student_id, section.pk)
        if r.startswith('failed'):
            return HttpResponse(r)
        d = json.loads(r)
        result[section.pk] = d
    
    return json.dumps(result)

def get_student_chapter_vector(request):
    if request.method != 'GET':
        return HttpResponse('failed: method should be get')

    student_id = request.GET.get('student_id', '')
    chapter_id = request.GET.get('chapter_id', '')

    return HttpResponse(get_student_chapter_vector_wrapper(student_id, chapter_id))

def get_cls_graph_vector(request):
    if request.method != 'GET':
        return HttpResponse('failed: method should be get')

    cls_id = request.GET.get('cls_id', '')
    graph_id = request.GET.get('graph_id', '')

    if not cls_id:
        return HttpResponse('failed: cls id missing')

    if not graph_id:
        return HttpResponse('failed: graph id missing')
        
    result = json.loads(get_cls_graph(cls_id, graph_id))
    if result['status'] == 'fail':
        return HttpResponse('failed: ' + result['reason'])

    return HttpResponse(json.dumps(result['data']))

def get_cls_section_vector_wrapper(cls_id, section_id):
    try:
        section = Section.objects.get(pk=section_id)
    except:
        return 'failed: section not exised'

    nodes_list = KnowledgeNode.objects.filter(pk__in=json.loads(section.nodes_list))

    graph_list = list(set(map(lambda x: x.graph, nodes_list)))

    result = {}

    for graph in graph_list:
        tmp = json.loads(get_cls_graph(cls_id, graph.pk))
        if tmp['status'] == 'fail':
            return 'failed: ' + tmp['reason']

        d = tmp['data'].copy()
        nl = json.loads(section.nodes_list)
        for key in tmp['data']:
            if key not in nl:
                d.pop(key)

        result[graph.pk] = d
    return json.dumps(result)

def get_cls_section_vector(request):
    if request.method != 'GET':
        return HttpResponse('failed: method should be get')

    cls_id = request.GET.get('cls_id', '')
    section_id = request.GET.get('section_id', '')

    return HttpResponse(get_cls_section_vector_wrapper(cls_id, section_id))

def get_cls_chapter_vector_wrapper(cls_id, chapter_id):
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
    except:
        return 'failed: chapter not existed'

    sections = chapter.sections.all()
    
    result = {}

    for section in sections:
        r = get_cls_section_vector_wrapper(cls_id, section.pk)
        if r.startswith('failed'):
            return HttpResponse(r)
        d = json.loads(r)
        result[section.pk] = d
    
    return json.dumps(result)

def get_cls_chapter_vector(request):
    if request.method != 'GET':
        return HttpResponse('failed: method should be get')

    cls_id = request.GET.get('cls_id', '')
    chapter_id = request.GET.get('chapter_id', '')

    return HttpResponse(get_cls_chapter_vector_wrapper(cls_id, chapter_id))
