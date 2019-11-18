from django.shortcuts import render
from webapps.parent.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
@csrf_exempt
def update_parent(request):
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id', '')
        name = request.POST.get('name','')
        info = request.POST.get('info','')
        phone = request.POST.get('phone','')
        student_id = request.POST.get('student_id','')
        if parent_id:
            parent = ParentProfile.objects.get(pk = parent_id)
            parent.name = name
            parent.info = info
            parent.phone = phone
            parent.save()
            return HttpResponse('OK')
        parent = ParentProfile(name=name, info=info, phone=phone)
        parent.save()
        parent.student.add(student_id)
        knowledge_node = request.GET.get('knowledge_node', '')
        return HttpResponse('OK')
    return HttpResponse('error method')
