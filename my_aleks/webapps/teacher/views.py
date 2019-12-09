# -*- coding:utf-8 -*-
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from webapps.school.models import Cls
from webapps.quiz.models import Quiz
from webapps.quiz.models import Question
from webapps.parent.models import ParentProfile
from webapps.quiz.models import QuizRecord
from webapps.quiz.models import QuizRecordPaper
from django.views.decorators.csrf import csrf_exempt
from webapps.knowledge_space.models import Subject
from webapps.student.models import StudentProfile,StudentReportPaper,StudentQuizRecord
from .models import *
# Create your views here.
import time
from django.contrib.auth import authenticate, login


@login_required
def index(request):
    if request.method == 'GET':
        user = request.user
        if not user.groups.filter(name='TEACHER').exists():
            return render(request,'teacher/errorPage.html',{"errorType":"用户权限不足","particulars":"fault:user is not a teacher"})
        class_id = request.GET.get('classId', '')
        student_id = request.GET.get('studentId', '')
        base_template = request.GET.get('template','')
        try:
            classes = user.teacherprofile.classes.filter(deleted=False)
            class_dics = list(classes.values('id', 'name'))
        except:
            class_dics=[]
            # return render(request,'teacher/errorPage.html',{"errorType":"用户数据不全","particulars":"fault:user has not class"})
        if class_id and student_id:
            if not base_template:
                if user.groups.filter(name="TEACHER").exists():
                    base_template='teacher/teacher_base.html'
                if user.groups.filter(name="SCHOOL_MANAGER").exists():
                    base_template='school/school_base.html'
            try:
                student=StudentProfile.objects.get(pk=student_id)
            except:
                return render(request,'teacher/errorPage.html',{"errorType":"参数错误","particulars":"fault:student not exists"})
            parentList = ParentProfile.objects.filter(student=student)
            studentProfile = {"profile":student,"parentList":parentList}
            #print("---------------------")
            #print(student)
            #print(parentList)
            try:
                cls = Cls.objects.get(pk=class_id,deleted=False)
            except:
                return render(request,'teacher/errorPage.html',{"errorType":"参数错误","particulars":"fault:class not exists"})
            try:
                student_quiz_record=student.studentreportpaper_set.all()
                student_quiz_record=student_quiz_record.filter(subject=cls.subject)
                student_quiz_record_dics = list(student_quiz_record.values('student__student_no', 'pdf_uri','datetime'))
            except:
                student_quiz_record_dics =[]
                #return render(request,'teacher/errorPage.html',{"errorType":"用户数据不全","particulars":"fault:student_quiz_record_paper not exists"})
            LearningInformation = {
                'reportList': student_quiz_record_dics,
            }
            #print(studentProfile)
            return render(request, 'teacher/index.html',
                          {'LearningInformation': LearningInformation, 'classes': class_dics,'base_template':base_template,'studentProfile':studentProfile})
        if class_id :
            try:
                cls = Cls.objects.get(pk=class_id,deleted=False)
            except:
                return render(request,'teacher/errorPage.html',{"errorType":"参数错误","particulars":"fault:class not exists"})
            if user!=cls.teacher.user:
                return render(request,'teacher/errorPage.html',{"errorType":"权限不足","particulars":"fault:user is not this class's teacher"})
            students = json.loads(cls.students)
            try:
                student_profiles = StudentProfile.objects.filter(student_no__in=students)
            except:
                return render(request,'teacher/errorPage.html',{"errorType":"用户数据紊乱","particulars":"fault:student_profile not exists"})

            students_list = []
            for student_profile in student_profiles:
                try:
                    is_join = False
                    if StudentQuizRecord.objects.filter(student=student_profile,quiz_record__cls=cls).exists():
                        is_join = True
                except:
                    is_join = False
                students_list.append({"student_no" : student_profile.student_no, "name" : student_profile.name, "id" : student_profile.pk,"is_join" : is_join})


            try:
                quizrecord = list(QuizRecord.objects.filter(cls=cls).order_by('-datetime').values('info'))
            except:
                #return render(request,'teacher/errorPage.html',{"errorType":"用户数据不全","particulars":"fault:quiz_record not exists"})
                pass
            try:
                info = json.loads(quizrecord[0]['info'])
                if info['average_score'] <= 1:
                    info['average_score'] = int(info['average_score'] * 100)
                if info['lowest_score'] < 1:
                    info['lowest_score'] = int(info['lowest_score'] * 100)
                if info['highest_score'] <= 1:
                    info['highest_score'] = int(info['highest_score'] * 100)
                # print (json.loads(student_profiles))
                LearningInformation = {
                    'performance': {
                        'averageScore': info['average_score'],
                        'lowestScore': info['lowest_score'],
                        'topScore': info['highest_score'],
                    },
                    'studentList': students_list
                }
            except:
                 LearningInformation = {
                    'studentList': students_list
                }                
        
            return render(request, 'teacher/index.html', {'LearningInformation': LearningInformation,'classes':class_dics,'base_template':'teacher/teacher_base.html'})
        return render(request, 'teacher/index.html', {'classes':class_dics,'base_template':'teacher/teacher_base.html'})
    return render(request, 'teacher/index.html',{'base_template':'teacher/teacher_base.html'})

@login_required
def my_quizes(request):
    '''
    see all quizes created by a user
    '''
    user=request.user
    if not user.groups.filter(name='TEACHER').exists():
        return render(request,'teacher/errorPage.html',{"errorType":"用户权限不足","particulars":"fault:user is not a teacher"})
    #quiz_record=user.quizrecord_set.all()
    try:
        quiz = user.quiz_set.all()
    except:
        return render(request, 'teacher/my_quizes.html')
    quiz_dicts = list(quiz.values('id', 'info', 'subject', 'generator','quiz_type','public'))
    for dic in quiz_dicts:
        try:
            dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
            dic['generator'] = user.username
            dic['info']=json.loads(dic['info'])
        except:
            pass
    return render(request, 'teacher/my_quizes.html',{'quizInfo':quiz_dicts})

@login_required
@csrf_exempt
def ajax_my_quizes(request):
    '''
    see all quizes created by a user
    '''
    user=request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse("fault:user is not a teacher")
    #quiz_record=user.quizrecord_set.all()
    try:
        quiz = user.quiz_set.all()
    except:
        return HttpResponse(json.dumps([]))
    quiz_dicts = list(quiz.values('id', 'info', 'subject', 'generator','quiz_type','public'))
    for dic in quiz_dicts:
        try:
            #dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
            dic['generator'] = user.username
            dic['info']=json.loads(dic['info'])
        except:
            pass
    return HttpResponse(json.dumps(quiz_dicts))
@login_required
@csrf_exempt
def ajax_get_user_img(request):
    user = request.user
    try:
        img=user.teacherprofile.img.url
    except:
        return HttpResponse('user no have teacherProfile')
    return HttpResponse(img)

@login_required
@csrf_exempt
def ajax_get_class_report_by_class_id(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    dic = json.loads(request.body.decode('utf-8'))
    class_id = dic["classId"]
    page = dic["page"]
    size = dic["size"]
    try:
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')
    quiz_records=cls.quizrecord_set.all()
    quiz_record_paper_dict=[]
    for quiz_record in quiz_records:
        quiz_record_papers=quiz_record.quizrecordpaper_set.all()
        for quiz_record_paper in quiz_record_papers:
            quiz_record_paper_dict.append({"id":quiz_record_paper.id,"pdf_uri":quiz_record_paper.pdf_uri})
    dict_length=len(quiz_record_paper_dict)
    # 分页操作
    hasNext=True
    if (page-1)*size>dict_length:
        return HttpResponse("page is error")
    else:
        if page*size < dict_length:
            quiz_record_dict=quiz_record_paper_dict[(page-1)*size:page*size]
        else:
            hasNext=False
            quiz_record_dict=quiz_record_paper_dict[(page-1)*size:]
    info={"hasNext":hasNext,"quiz_record":quiz_record_dict}
    return HttpResponse(json.dumps(info))

@login_required
@csrf_exempt
def ajax_get_scores_student(request):
    dic = json.loads(request.body.decode('utf-8'))
    class_id = dic["classId"]
    student_id = dic["studentId"]
    try:
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')
    quiz_records=cls.quizrecord_set.all()
    student=StudentProfile.objects.get(pk=student_id)
    student_quiz_record=list(StudentQuizRecord.objects.filter(student=student,quiz_record__in=quiz_records).order_by("-datetime").values("datetime","score"))
    if len(student_quiz_record)>8:
        student_quiz_record=student_quiz_record[0:8]
    scores=[]
    times=[]
    for index in student_quiz_record:
        if index['score'] <= 1:
            scores.append(index['score']*100)
        else:
            scores.append(index['score'])
        times.append(index['datetime'].strftime('%Y-%m-%d'))
    scores.reverse()
    times.reverse()
    return HttpResponse(json.dumps({"score":scores,"time":times}))

@login_required
@csrf_exempt
def ajax_get_scores_class(request):
    dic =json.loads(request.body.decode('utf-8'))
    class_id = dic['classId']
    try:
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')
    quiz_record_dics=list(cls.quizrecord_set.all().order_by('-datetime').values('datetime','info'))
    if len(quiz_record_dics)>8:
        quiz_record_dics=quiz_record_dics[0:8]
    scores = []
    times = []
    for quiz_record in quiz_record_dics:
        quiz_record_info = json.loads(quiz_record['info'])
        if 'average_score' in quiz_record_info:
            score = quiz_record_info['average_score']
            if score <= 1:
                score=score*100
            scores.append(score)
            times.append(quiz_record['datetime'].strftime('%Y-%m-%d'))
    scores.reverse()
    times.reverse()
    return HttpResponse(json.dumps({"score":scores,"time":times}))
@login_required
@csrf_exempt
def ajax_update_teacher_profile(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    dic = json.loads(request.body.decode('utf-8'))
    name=dic['name']
    phone=dic['phone']
    info=dic['info']
    try:
        teacher_profile=user.teacherprofile
    except:
        return HttpResponse('user have not  teacherProfile')
    teacher_profile.name=name
    teacher_profile.info=info
    teacher_profile.phone=phone
    try:
        teacher_profile.save()
    except:
        return HttpResponse('save failed')
    return HttpResponse('success')

@login_required
def view_class(request):
    if request.method == 'POST':
        return HttpResponse('wrong method, should be GET')

    class_id = request.GET.get('class_id', '')
    if not class_id:
        return HttpResponse('no class_id')
    try:
        cls = Cls.objects.get(pk=class_id,deleted=False)
    except:
        return HttpResponse('class not existed')

    student_list = json.loads(cls.students)
    students = User.objects.filter(pk__in=student_list)

    return render(request, 'teacher/class.html', {'class': cls, 'students':students})



@login_required
def view_teacher_profile(request):
    if request.method == 'POST':
        return HttpResponse('wrong method, should be GET')
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    try:
        teacher = user.teacherprofile
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:teacher profile not existed"})
        
    try:
        classes = user.teacherprofile.classes
        classes = classes.filter(deleted=False)
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:class not existed"})
    try:
        subject=Subject.objects.get(name=teacher.subject_id).chinese_name
    except:
        return HttpResponse(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:subject not existed"})
    try:
        school = teacher.school.name
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:school not existed"})
    teacherFileList = TeacherFile.objects.filter(teacher=teacher)
    #try:
     #   teacherFileList = TeacherFile.object.filter(teacher=teacher)
    #except:
    #     return render(request,'teacher/errorPage.html',{"errorType":"查询错误","particulars":"fault:system error"})
    menuNum = {}
    menuNum['classNum'] = len(classes.all())
    quizList = Quiz.objects.filter(generator=user)
    menuNum['quizNum'] = len(quizList)
    questionList = Question.objects.filter(uploader=user)
    menuNum['questionNum'] = len(questionList)
    favorites = Favorites.objects.filter(teacher=teacher)
    menuNum['favorites'] = len(favorites.first().questions.all())
    return render(request, 'teacher/teacher_profile.html', {'teacherProfile':{'menuNum':menuNum,'teacher':teacher,'subject':subject,'classes':classes.all(),'school':school,'teacherFiles':teacherFileList.all()}})





@login_required
@csrf_exempt
def ajax_my_classes(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    try:
        classes = user.teacherprofile.classes
        classes = classes.filter(deleted=False)
    except:
        return HttpResponse("fault:class not existed")
    class_dicts = []
    for cls in classes.all():
        subject=Subject.objects.get(name=cls.subject).chinese_name
        class_dicts.append({"id":cls.id,"name":cls.name,"grade":cls.grade,"num":cls.num,"subject":subject})
    return HttpResponse(json.dumps(class_dicts))

@login_required
def my_classes(request):
    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    #try:
    #    classes = user.teacherprofile.classes
    #except:
    #    return render(request,'teacher/errorPage.html',{"errorType":"数据缺失","particulars":"fault:class not existed"})
    #class_dicts = []
    #for cls in classes.all():
    #    subject=Subject.objects.get(name=cls.subject).chinese_name
    #    class_dicts.append({"id":cls.id,"name":cls.name,"grade":cls.grade,"num":cls.num,"subject":subject})
    return render(request, 'teacher/my_classes.html')




#@login_required
#def view_student(request):
#    return render(request, 'teacher/student.html')

@login_required
@csrf_exempt
def upload_teacher_img(request):
    if request.method == 'POST':
        try:
            img = request.FILES['img']
        except:
            return HttpResponse('failed: no image')
        profile_id = request.POST.get('profile_id', '')
        try:
            teacher_profile = TeacherProfile.objects.get(pk=profile_id)
        except:
            return HttpResponse('failed: profile not existed')

        teacher_profile.img = img
        teacher_profile.save()
        return HttpResponse('OK')
    
    if request.method == 'GET':
        return HttpResponse('wrong method, should be POST')

@login_required
@csrf_exempt
def upload_teacherfile(request):
    if request.method == 'POST':
        try:
            img = request.FILES['img']
        except:
            return HttpResponse('failed: no image')
        profile_id = request.POST.get('profile_id', '')
        try:
            teacher_profile = TeacherProfile.objects.get(pk=profile_id)
        except:
            return HttpResponse('failed: profile not existed')
        description = request.POST.get('description')
        teacherFile = TeacherFile.objects.create(teacher=teacher_profile,description=description,img=img);
        teacherFile.save()
        return HttpResponse('OK')
    
    if request.method == 'GET':
        return HttpResponse('wrong method, should be POST')
 
@csrf_exempt
def teacher_login(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        username = json.loads(body)['username']
        password = json.loads(body)['password']
        user = authenticate(request = request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username']=username
            teacher = user.teacherprofile
            school = teacher.school
            img = ''
            if teacher.img:
                img = teacher.img.url
            return HttpResponse(json.dumps({"status":True,"teacher":{"id":teacher.id, "img":img, "name":teacher.name, "info":teacher.info, "phone":teacher.phone, "subject":teacher.subject.chinese_name, "user_id":user.id,"school":{"id":school.id, "name":school.name}}}))
        else:
            return HttpResponse(json.dumps({"status":False}))
@login_required
@csrf_exempt
def ajax_teacher_profile(request):
    if request.method == 'POST':
        return HttpResponse('wrong method, should be GET')

    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')

    try:
        teacher = user.teacherprofile
    except:
        return HttpResponse("fault:teacher profile not existed")
        
    try:
        subject=Subject.objects.get(name=teacher.subject_id).chinese_name
    except:
        return HttpResponse("fault:subject not existed")
    try:
        school = teacher.school
    except:
        return HttpResponse("fault:school not existed")
    img = ''
    if teacher.img:
        img = teacher.img.url
    return HttpResponse(json.dumps({"id":teacher.id, "img":img, "info":teacher.info, "name":teacher.name, "phone":teacher.phone, "school":school.name, "user_id":user.id,"school":{"id":school.id, "name":school.name},"subject":subject}))

@login_required
@csrf_exempt
def student_tuition(request):
    if request.method == 'POST':
        return HttpResponse('wrong method, should be GET')
    model = request.GET.get('model','')
    user = request.user
    cls_id = request.GET.get('cls_id','')
    if user.groups.filter(name="SCHOOL_MANAGER").exists():
        base_template='school/school_base.html'
        school = user.school
        classes = school.classes
    else:
        if user.groups.filter(name="TEACHER").exists():
            try:
                base_template='teacher/teacher_base.html'
                classes = user.teacherprofile.classes
                classes = classes.filter(deleted=False)
            except:
                return HttpResponse("fault:class not existed")
        else:
            return HttpResponse("user not teacher or school")
    class_dicts = classes.all()
    if model != '':
        if model == 'teacher':
            base_template='teacher/teacher_base.html'
        else:
            base_template='school/school_base.html'
    if cls_id :
        try:
            cls = classes.get(pk = cls_id)
            subject = Subject.objects.get(pk = cls.subject).chinese_name
            teacher = cls.teacher.name
        except:
            return HttpResponse("fault:class_id not existed")
        students = json.loads(cls.students)
        student_profiles = StudentProfile.objects.filter(student_no__in=students)
        return render(request, 'teacher/student_tuition.html',{'base_template':base_template,'classList':class_dicts,'ClassInformation':student_profiles,'nowClass':cls,'subject':subject,'teacher':teacher});
    return render(request, 'teacher/student_tuition.html',{'base_template':base_template,'classList':class_dicts});



@login_required
@csrf_exempt
def my_schedule(request):
    if request.method == 'POST':
        return HttpResponse('wrong method, should be GET')
    user = request.user
    cls_id = request.GET.get('cls_id','')
    if user.groups.filter(name="SCHOOL_MANAGER").exists(): 
        base_template='school/school_base.html'
        school = user.school
        classes = school.classes
        class_dicts = classes.all()
        return render(request, 'school/class_schedule.html',{'base_template':base_template,'classList':class_dicts});
    else:
        if user.groups.filter(name="TEACHER").exists():
            base_template='teacher/teacher_base.html'
            try:
                classes = user.teacherprofile.classes
                classes = classes.filter(deleted=False)
            except:
                return HttpResponse("fault:class not existed")
        else:
            return HttpResponse("user not teacher or school")
        class_dicts = classes.all()
        return render(request, 'teacher/my_schedule.html',{'base_template':base_template,'classList':class_dicts});

