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
from django.db import transaction
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

    # student_id means profile id
    try:
        student_id = dic['studentId']
        class_id = dic['clsId']
    except:
        return HttpResponse('failed: missing data')

    try:
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')

    try:
        student = StudentProfile.objects.get(student_no=student_id)
    except:
        return HttpResponse('student not existed')

    if not cls.teacher.user == user:
        if not cls.school.manager == user:
            return HttpResponse('no right to add student')
    
    #student = User.objects.get(pk=student_id)
    students = json.loads(cls.students)
    if not str(student_id) in students:
        students.append(str(student_id))
    cls.num = len(students)
    cls.students = json.dumps(students)

    classes = json.loads(student.cls_list)
    if not str (class_id) in classes:
        classes.append(str(class_id))
    student.cls_list=json.dumps(classes)

    try:
        plan=Plan.objects.get(cls=cls)
    except:
        return HttpResponse('class have not plan')
    student_plan=StudentPlan(student=student,price=plan.price,plan=plan,payment_record="SCHOOL",paid=False,cls=cls,resources=plan.resources,remaining_resources=plan.resources,description=plan.description,subject=plan.subject,info={})
    try:
        with transaction.atomic():
            student_plan.save()
            student.save()
            cls.save()
    except:
        return HttpResponse('save plan failed')
    return HttpResponse('OK')

@login_required
def add_class(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')

    #TODO: class form
    return HttpResponse('OK')

@login_required
def get_teachers(request):
    user = request.user
    if not user.groups.filter(name='SCHOOL_MANAGER').exists():
        return HttpResponse("user is not a school manager")
    try:
        school = user.school
    except:
        return HttpResponse('user has not school')
    teachers = school.teacherprofile_set.all()
    return render(request,'school/school_teacher.html',{'teachers':teachers})

@login_required
def get_classes(request):
    teacher_id=request.GET.get('teacherId','')
    user = request.user
    if not user.groups.filter(name='SCHOOL_MANAGER').exists():
        return HttpResponse('user is not a school manager')
    '''
    try:
        school = user.school
    except:
        return HttpResponse('user has not school')

    classes = school.classes.all()
    if teacher_id:
        classes = classes.filter(teacher__id=teacher_id)
    
    classes_dicts = list(classes.values('id', 'name', 'subject', 'grade', 'teacher__name', 'num'))
    for dic in classes_dicts:
        try:
            dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
        except:
            pass
    '''
    return render(request, 'school/school_cls.html',{'teacherId':teacher_id})

@login_required
@csrf_exempt
def ajax_get_cls(request):
    teacher_id=request.GET.get('teacherId','')

    user = request.user
    if not user.groups.filter(name='SCHOOL_MANAGER').exists():
        return HttpResponse('user is not a school manager')

    try:
        school = user.school
    except:
        return HttpResponse('user has not school')

    classes = school.classes.all()
    if teacher_id:
        classes = classes.filter(teacher__id=teacher_id)
    classes=classes.filter(deleted=False)
    classes_dicts = list(classes.values('id', 'name', 'subject', 'grade', 'teacher__name', 'num'))
    for dic in classes_dicts:
        try:
            dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
        except:
            pass
    return HttpResponse(json.dumps({'classes': classes_dicts, 'schoolId': school.pk}))

    #return HttpResponse("test")

@login_required
@csrf_exempt
def ajax_get_own_classes(request):
    user = request.user
    if not user.groups.filter(name="TEACHER").exists():
        return HttpResponse("user is not teacher")
    try:
        classes=Cls.objects.filter(teacher=user.teacherprofile,deleted=False)
    except:
        return HttpResponse('cls not existed')
    cls_dist={}
    for cls in classes:
        cls_dist[cls.id]=cls.name
    return HttpResponse(json.dumps(cls_dist))
@login_required
@csrf_exempt
def ajax_get_school_name(request):
    user = request.user
    if not user.groups.filter(name="SCHOOL_MANAGER").exists():
        return HttpResponse('user is not a school manager')
    try:
        school = user.school
    except:
        return HttpResponse('user has not school')
    return HttpResponse(school.name)
@login_required
def get_class_detail(request):
    if request.method != 'GET':
        return HttpResponse('wrong method')

    user = request.user
    cls_id = request.GET.get('clsId')
    try:
        #use filter to take use of queryset's values function
        cls = Cls.objects.filter(pk=cls_id,deleted=False)
    except:
        return HttpResponse('class not existed')

    class_info = list(cls.values('id', 'name', 'subject', 'grade', 'teacher__name', 'num'))[0]
    
    try:
        class_info['subject'] = Subject.objects.get(name=class_info['subject']).chinese_name
        #print(nodes_list)
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
    student_profiles = StudentProfile.objects.filter(student_no__in=students)
    student_list=[]
    for student in student_profiles:
        try:
            student_plan = StudentPlan.objects.filter(student=student,cls=cls)[0]
            stuPlanId=student_plan.id
            payStatus=student_plan.paid
        except:
            stuPlanId=''
            payStatus=''
        student_list.append({'stuPlanId':stuPlanId,"payStatus":payStatus,"id":student.id,"student_no":student.student_no,"name":student.name})

    if user.groups.filter(name='TEACHER').exists():
        try:
            teacher = cls.teacher.user
            if teacher == user:
                return render(request, 'school/school_cls_detail.html', {'planInfo': plan_info, 'students': student_list, 'clsInfo':class_info,'base_template':'teacher/teacher_base.html'})
        except:
            pass
        

    if user.groups.filter(name='SCHOOL_MANAGER').exists():
        try:
            school = user.school
            if cls.school == school:
                return render(request, 'school/school_cls_detail.html', {'planInfo': plan_info, 'students': student_list, 'clsInfo':class_info,'base_template':'school/school_base.html'})
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
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')

    try:
        student = StudentProfile.objects.get(student_no=student_id)
    except:
        return HttpResponse('student not existed')

    if not cls.teacher.user == user:
        if not cls.school.manager == user:
            return HttpResponse('no right to add student')
    
    #student = User.objects.get(pk=student_id)
    students = json.loads(cls.students)
    if str(student_id) in students:
        students.remove(str(student_id))
    cls.num = len(students)
    cls.students = json.dumps(students)
    cls.save()
    classes = json.loads(student.cls_list)
    if str(class_id) in classes:
        classes.remove(str(class_id))
    student.cls_list=json.dumps(classes)
    student.save()
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
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')

    if not cls.school.manager == user:
        return HttpResponse('no right to add student')

    try:
        student_plan = StudentPlan.objects.get(pk=student_plan_id)
    except:
        return HttpResponse('student plan not created')

    student_id = student_plan.student.student_no

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
def delete_class(request):
    user = request.user
    cls_id = request.GET.get('cls_id','')
    with transaction.atomic():
        try:
            cls = Cls.objects.get(pk=cls_id,deleted=False)
        except:
            return HttpResponse('faield, class not existed')
        students=json.loads(cls.students)
        if students==[]:
            cls.delete()
        else:
            for student in students:
                studentProfile=StudentProfile.objects.get(id=student)
                classes = json.loads(studentProfile.cls_list)
                if cls_id in classes:
                    classes.remove(cls_id)
                studentProfile.cls_list=json.dumps(classes)
                studentProfile.save()
                cls.deleted=True
                cls.save()
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



@login_required
def school_profile(request):
    if request.method == "POST":
        return HttpResponse('wrong method, should be GET')
    user = request.user
    if not user.groups.filter(name="SCHOOL_MANAGER").exists():
        return HttpResponse('user is not a manager')
    try:
        school = user.school
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:school profile not existed1"})
    
    try:
        classes = user.school.classes.all().filter(deleted=False)
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:school profile not existed2"})
    try:
        teachers=TeacherProfile.objects.filter(school=school)  
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:school profile not existed3"})
    return render(request,'school/school_profile.html', {'schoolProfile':{'school':school,'classes':len(classes),'classesList':classes,'teacher':len(teachers)}})


@login_required
@csrf_exempt
def ajax_update_school(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    dic = json.loads(request.body.decode('utf-8'))
    name = dic['name']
    phone = dic['phone']
    location = dic['location']
    try:
        school = user.school
    except:
        return HttpResponse('user have not  SchoolProfile')
    school.name = name
    school.phone = phone
    school.location = location
    try:
        school.save()
    except:
        return HttpResponse('save failed')
    return HttpResponse('OK')
    
@login_required
@csrf_exempt
def upload_school_img(request):
    if request.method == 'POST':
        try:
            img = request.FILES['img']
        except:
            return HttpResponse('failed: no image')
        school_id = request.POST.get('school_id', '')
        try:
            school = School.objects.get(pk=school_id)
        except:
            return HttpResponse('failed: school not existed')

        school.img = img
        school.save()
        return HttpResponse('OK')
    
    if request.method == 'GET':
        return HttpResponse('wrong method, should be POST')


@login_required
@csrf_exempt
def ajax_get_school_img(request):
    school_id = request.GET.get('school_id', '')
    try:
        school = School.objects.get(pk=school_id)
    except:
        return HttpResponse('failed: school not existed')

    try:
        img = school.img.url
    except:
        return HttpResponse('failed: school has no img')

    return HttpResponse(img)

