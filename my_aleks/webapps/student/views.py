# -*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import *


# Create your views here.


@login_required
def student_index(request):
    return render(request, 'student/student_index.html')

@csrf_exempt
def student_login(request):
    '''
        input: json dict of username and password
        output: result and error reason
    '''
    d = {}
    if request.method == 'GET':
        return HttpResponse('wrong method', status=400)

    body = request.body.decode('utf-8')

    try:
        username = json.loads(body)['username']
        password = json.loads(body)['password']
    except:
        d['status'] = False
        d['errorReason'] = 'field missing'
        return HttpResponse(json.dumps(d))
        
    #print(request.body)
    #username = request.POST.get('username', '')
    #password = request.POST.get('password', '')
    user = authenticate(request=request, username=username, password=password)
    #print(username)
    #print(password)
    if user is not None:
        if not user.groups.filter(name='STUDENT').exists(): 
            d['status'] = False
            d['errorReason'] = 'user is not a student'
            return HttpResponse(json.dumps(d))
            
        login(request, user)
        d['status'] = True
        d['errorReason'] = ''
        try:
            p = user.studentprofile
            dd = p.__dict__
            del dd['_state']
            del dd['_user_cache']
            d['student'] = dd
        except:
            d['student'] = None
        return HttpResponse(json.dumps(d))

    else:
        d['status'] = False
        try:
            user = User.objects.get(username=username)
        except:
            d['errorReason'] = 'user not existed'
            return HttpResponse(json.dumps(d))
        d['errorReason'] = 'login failed'
        return HttpResponse(json.dumps(d))

@login_required
def student_register(request):
    if request.method == 'GET':
        return render(request, 'portal/register.html')
    else:
        username = request.POST.get('username', '')
        if not username:
            return HttpResponse('no student username info')
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('student account not existed')

        # necessary fields
        phone = request.POST.get('phone', '')
        name = request.POST.get('name', '')

        if not name:
            return HttpResponse('no name provided')
        if not phone:
            return HttpResponse('no phone provided')

        try:
            profile = StudentProfile.objects.create(user=user, phone=phone, name=name)
        except:
            return HttpResponse('create profile failed')

        info = {}

        school = request.POST.get('school', '')
        grade = request.POST.get('grade', '')
        gender = request.POST.get('gender', '')
        province = request.POST.get('province', '')
        city = request.POST.get('city', '')
        district = request.POST.get('district', '')

        if school:
            info['school'] = school
        if grade:
            info['grade'] = grade
        if gender:
            info['gender'] = gender
        if province:
            info['province'] = province
        if city:
            info['city'] = city
        if district:
            info['district'] = district
        
        info = json.dumps(info)

        profile.info = info
        profile.save()

        return HttpResponse('OK')

# 获取评估
@login_required
def get_assessment(request):
    return render(request, 'student/student_assessment.html')

@login_required
def student_quiz_report(request):
    return render(request, 'student/student_quiz_report.html')

@login_required
def ajax_get_student_profile(request):
    phone = request.GET.get('phone', '')
    student_no = request.GET.get('student_no', '')
    if (not phone) and (not student_no):
        return HttpResponse('failed')

    if phone:
        try:
            p = StudentProfile.objects.get(phone = phone)
        except:
            return HttpResponse('failed: user not existed')

    else:
        try:
            p = StudentProfile.objects.get(student_no = student_no)
        except:
            return HttpResponse('failed: user not existed')

    dic = {'name': p.name, 'student_id': p.pk, 'age': p.age, 'phone':p.phone, 'student_no': p.student_no, 'gender': p.gender}

    return HttpResponse(json.dumps(dic))

@login_required
def student_profile_tuition(request):
    return render(request, 'student/student_tuition.html')



