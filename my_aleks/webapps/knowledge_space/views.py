from .batch_input import *
from django.views.decorators.csrf import csrf_exempt

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

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
def ajax_upload_edge(request):
    if request.method == 'GET':
        return HttpResposne(status=400)

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


