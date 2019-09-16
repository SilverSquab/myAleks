from django.shortcuts import render
from webapps.knowledge_space.models import Subject
from webapps.teacher.models import TeacherProfile
from webapps.plan.models import *
from webapps.student.models import StudentProfile
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import json
from .models import *

# Create your views here.

def school_index(request):
    pass

@login_required
@csrf_exempt
def add_student_to_class(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    
    dic = json.loads(request.body.decode('utf-8'))
    try:
        student_id = dic['studentId']
        class_id = dic['clsId']
    except:
        return HttpResponse('failed: missing data')

    try:
        cls = Cls.objects.get(pk=class_id)
    except:
        return HttpResponse('class not existed')

    try:
        student = User.objects.get(pk=student_id)
    except:
        return HttpResponse('student not existed')

    if not cls.teacher == user:
        if not cls.school.manager == user:
            return HttpResponse('no right to add student')
    
    #student = User.objects.get(pk=student_id)
    students = json.loads(cls.students)
    if not str(student_id) in students:
        students.append(str(student_id))
    cls.num = len(students)
    cls.students = json.dumps(students)
    cls.save()

    return HttpResponse('OK')

@login_required
def add_class(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')

    #TODO: class form
    return HttpResponse('OK')

@login_required
def get_classes(request):
    user = request.user
    if not user.groups.filter(name='SCHOOL_MANAGER').exists():
        return HttpResponse('user is not a school manager')

    try:
        school = user.school
    except:
        return HttpResponse('user has not school')

    classes = school.classes.all()
    
    classes_dicts = list(classes.values('id', 'name', 'subject', 'grade', 'teacher__name', 'num'))
    for dic in classes_dicts:
        try:
            dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
        except:
            pass
    return render(request, 'school/school_cls.html', {'classes': classes_dicts, 'schoolId': school.pk})

    
@login_required
def get_class_detail(request):
    if request.method != 'GET':
        return HttpResponse('wrong method')

    user = request.user
    cls_id = request.GET.get('clsId')
    try:
        #use filter to take use of queryset's values function
        cls = Cls.objects.filter(pk=cls_id)
    except:
        return HttpResponse('class not existed')

    class_info = list(cls.values('id', 'name', 'subject', 'grade', 'teacher__name', 'num'))[0]
    
    try:
        class_info['subject'] = Subject.objects.get(name=class_info['subject']).chinese_name
    except:
        pass
    
    cls = cls[0]
    
    plans = cls.plan_set.all()
    if len(plans) == 0:
        plan_info = None
    else:
        plan_info = list(plans.values('info', 'description', 'resources'))[0]
    
    #TODO: get students info
    students = json.loads(cls.students)
    student_profiles = StudentProfile.objects.filter(pk__in=students)
    
    if user.groups.filter(name='TEACHER').exists():
        try:
            teacher = cls.teacher
            if teacher == user:
                return render(request, 'school/school_cls_detail.html', {'planInfo': plan_info, 'students': student_profiles, 'clsInfo':class_info})
        except:
            pass
        

    if user.groups.filter(name='SCHOOL_MANAGER').exists():
        try:
            school = user.school
            if cls.school == school:
                return render(request, 'school/school_cls_detail.html', {'planInfo': plan_info, 'students': student_profiles, 'clsInfo':class_info})
        except:
            pass

    return HttpResponse('class do not belong to current user')

@login_required
@csrf_exempt
def remove_student_from_class(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    
    dic = json.loads(request.body.decode('utf-8'))
    try:
        student_id = dic['studentId']
        class_id = dic['clsId']
    except:
        return HttpResponse('failed: missing data')

    try:
        cls = Cls.objects.get(pk=class_id)
    except:
        return HttpResponse('class not existed')

    try:
        student = User.objects.get(pk=student_id)
    except:
        return HttpResponse('student not existed')

    if not cls.teacher == user:
        if not cls.school.manager == user:
            return HttpResponse('no right to add student')
    
    #student = User.objects.get(pk=student_id)
    students = json.loads(cls.students)
    if str(student_id) in students:
        students.remove(str(student_id))
    cls.num = len(students)
    cls.students = json.dumps(students)
    cls.save()

    return HttpResponse('OK')

@login_required
@csrf_exempt
def pay_student_plan(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')

    dic = json.loads(request.body.decode('utf-8'))

    try:
        student_plan_id = dic['studentPlanId']
        class_id = dic['clsId']
    except:
        return HttpResponse('failed: missing data')

    try:
        cls = Cls.objects.get(pk=class_id)
    except:
        return HttpResponse('class not existed')

    if not cls.school.manager == user:
        return HttpResponse('no right to add student')

    try:
        student_plan = StudentPlan.objects.get(pk=student_plan_id)
    except:
        return HttpResponse('student plan not created')

    student_id = student_plan.student.user.pk

    students = json.loads(cls.students)
    if str(student_id) not in students:
        return HttpResponse('student not in this class')
    
    price = student_plan.price

    if student_plan.paid:
        return HttpResponse('failed: already paid')

    if user.school.account < price:
        return HttpResponse('account not enough')

    school = user.school

    school.account -= price
    student_plan.paid = True
    student_plan.payment_record = 'SCHOOL'
    
    student_plan.save()
    school.save()
    
    return HttpResponse('OK')

@login_required
@csrf_exempt
def create_class(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')

    dic = json.loads(request.body.decode('utf-8'))

    try:
        school = user.school
    except:
        return HttpResponse('user has no school')

    try:
        subject = dic['subject']
        grade = dic['grade']
        name = dic['name']
        teacher_id = dic['teacherId']
    except:
        return HttpResponse('faield: missing field')

    try:
        teacher = TeacherProfile.objects.get(pk=teacher_id)
    except:
        return HttpResponse('faield, teacher not existed')

    if teacher.school != user.school:
        return HttpResponse('failed, teacher not belong to this school')

    try:
        cls = Cls(subject = subject, grade = grade, name = name, teacher = teacher, school = user.school)
        cls.save()
    except:
        return HttpResponse('creating class failed')

    return HttpResponse('OK')

@login_required
@csrf_exempt
def get_all_teachers(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    
    try:
        school = user.school
    except:
        return HttpResponse('user has no school')

    teachers = list(school.teacherprofile_set.all().values_list('name', 'id'))

    return HttpResponse(json.dumps(teachers))