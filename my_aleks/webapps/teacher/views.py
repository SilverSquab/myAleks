# -*- coding:utf-8 -*-
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from webapps.school.models import Cls
from webapps.quiz.models import Quiz
from webapps.knowledge_space.models import Subject
# Create your views here.


@login_required
def index(request):
    return render(request, 'teacher/index.html')

@login_required
def my_quizes(request):
    '''
    see all quizes created by a user
    '''
    user=request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    try:
        quiz = user.quiz_set.all()
    except:
        return HttpResponse('user has not quiz')
    print(quiz)
    quiz_dicts = list(quiz.values('id', 'info', 'subject', 'generator'))
    for dic in quiz_dicts:
        try:
            dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
            dic['generator'] = user.username
            dic['info']=json.loads(dic['info'])
        except:
            pass
    return render(request, 'teacher/my_quizes.html',{'quizInfo':quiz_dicts})

@login_required
def view_class(request):
    if request.method == 'POST':
        return HttpResponse('wrong method, should be GET')

    class_id = request.GET.get('class_id', '')
    if not class_id:
        return HttpResponse('no class_id')
    try:
        cls = Cls.objects.get(pk=class_id)
    except:
        return HttpResponse('class not existed')

    student_list = json.loads(cls.students)
    students = User.objects.filter(pk__in=student_list)

    return render(request, 'teacher/class.html', {'class': cls, 'students':students})

@login_required
def my_classes(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    
    classes = user.teacherprofile.classes


    return render(request, 'teacher/my_classes.html', {'classes': classes})

@login_required
def view_student(request):
    return render(request, 'teacher/student.html')
