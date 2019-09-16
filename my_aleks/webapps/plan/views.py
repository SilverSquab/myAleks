from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.http import HttpResponse
from webapps.school.models import Cls
from .helpers import create_plan_from_template
from django.views.decorators.csrf import csrf_exempt   

# Create your views here.

@login_required
def ajax_get_plan_templates(request):
    plan_templates = PlanTemplate.objects.all()
    dic = list(plan_templates.values('id', 'description', 'resources', 'subject', 'info', 'default_price', 'name'))

    return HttpResponse(json.dumps(dic))


@login_required
@csrf_exempt
def assign_plan_to_class(request):
    if request.method == 'GET':
        return HttpResponse('wrong method, use post')

    user = request.user
    if not user.groups.filter(name='SCHOOL_MANAGER').exists():
        return HttpResponse('user is not a school manager')

    dic = json.loads(request.body.decode('utf-8'))

    try:
        pt_id = dic['planTemplateId']
        class_id = dic['clsId']
    except:
        return HttpResponse('failed: missing field')
    try:
        plan_template = PlanTemplate.objects.get(pk=pt_id)
    except:
        return HttpResponse('plan template not existed')

    try:
        cls = Cls.objects.get(pk=class_id)
    except:
        return HttpResponse('class not existed')

    if cls.school != user.school:
        return HttpResponse('class not belong to this user')

    if create_plan_from_template(plan_template, cls):
        return HttpResponse('OK')

    return HttpResponse('failed to create plan')
