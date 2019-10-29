#coding=utf-8
from webapps.quiz.helpers import answers_to_nodes, mark_quiz_wrapper
from webapps.knowledge_space.student_vector import get_node_scores
from webapps.knowledge_space.node_update import update_nodes
from webapps.knowledge_space.helpers import *
from webapps.student.models import StudentProfile, StudentQuizRecord
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from django.forms import DateInput, DateField, Form, Select, SelectMultiple, ModelForm, Textarea, TextInput, MultipleChoiceField, FileInput, CheckboxInput
from django.contrib.admin.views.decorators import staff_member_required
from webapps.knowledge_space.models import *
from webapps.textbook.models import *
from webapps.school.models import Cls
from webapps.teacher.models import TeacherProfile

from django import forms
import datetime
import requests
from webapps.knowledge_space.student_vector import get_or_create_graph_vector
# Create your views here.

class QuestionQueryForm(forms.Form):
    date = DateField(widget=TextInput(attrs={'class': 'datepicker'}))

    node = forms.CharField(widget=TextInput(attrs={'class': 'form-control bg-light', 'id': 'nodeSearchBar', 'placeholder': '知识点'}))
    subject_str = forms.CharField(widget=TextInput(attrs={'class': 'form-control bg-light', 'id': 'subject-str', 'placeholder': '科目'}))

    #node = forms.CharField(max_length=100)

# 定向检索题目，根据科目、知识点等
@login_required
def get_questions(request):
    pass

@login_required
def question_detail(request):
    pass

@login_required
def quiz_page(request):
    '''
    Technically this page if for teachers only. 
    A teacher can see his or her quizes. Whether a quiz can be published is to be decided.
    Only exception would be that staffs can also see a quiz.
    '''
    if request.method !='GET':
        return render(request,'teacher/errorPage.html',{"errorType":"调用方法错误","particulars":"fault:wrong method"})
    user=request.user
    school_name=TeacherProfile.objects.get(user=user).school.name
    quiz_id = request.GET.get('quizId','')
    quiz_record_id=request.GET.get('quizRecordId','')
    try:
        info=''
        if quiz_id:
            quiz = Quiz.objects.get(pk=quiz_id)
        if quiz_record_id:
            quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
            quiz=quiz_record.quiz
            info=json.loads(quiz_record.info)
    except:
        return render(request,'teacher/errorPage.html',{"errorType":"试卷查询失败","particulars":"fault:quiz not exsited"})
    try:
        quiz.subject = Subject.objects.get(name=quiz.subject).chinese_name
    except:
        pass
    quiz.info=json.loads(quiz.info)
    quiz_paper_url=''
    try:
        quiz_paper_url=quiz.quizpaper_set.all()[0].pdf_uri
    except:
        pass
    #print(quiz)
    quiz_body = json.loads(quiz.body)
    questions =[]
    #print(quiz_body)
    for body in quiz_body:
        # print(quiz_body[body][0])
        try:
            correct_rate=info['correctRate'][body]
        except:
            correct_rate=''
        try:
            question = Question.objects.get(pk = quiz_body[body][0])
        except:
            return render(request,'teacher/errorPage.html',{"errorType":"数据紊乱","particulars":"fault:question not exsited"})
        try:
            options = question.options.all().order_by('order')
        except:
            return render(request,'teacher/errorPage.html',{"errorType":"数据紊乱","particulars":"fault:option not exsited"})
        options_dicts = list(options.values('body','order','img','is_correct'))
        for option in options_dicts:
            if option["is_correct"]:
                true_option=option['order']
        knowledge_node = KnowledgeNode.objects.filter(question=question)
        questions.append({'question':question,'options':options,"knowledge_nodes":knowledge_node,'true_option':true_option,"correct_rate":correct_rate})
    return render(request, 'quiz/quiz_detail.html',{"quizInfo":quiz,'questions':questions,'quiz_paper_url':quiz_paper_url,"info":info,"quiz_record_id":quiz_record_id,'school':school_name})

@login_required
def quiz_records(request):
    '''
    Only visited by teacher.
    See his or her quiz records.
    '''
    user=request.user
    if not user.groups.filter(name='TEACHER').exists():
        return render(request,'teacher/errorPage.html',{"errorType":"用户权限不足","particulars":"fault:user is not a teacher"})
    #teacher=user.teacher
    #quiz_records=teacher.quizrecord_set.all()
    quiz_records=QuizRecord.objects.filter(teacher__user=user)
    quiz=[]
    for quiz_record in quiz_records:
        subject=Subject.objects.get(name=quiz_record.quiz.subject).chinese_name
        info = json.loads(quiz_record.quiz.info)
        generator = quiz_record.quiz.generator.username
        cls = quiz_record.cls.name
        quiz_record_info=json.loads(quiz_record.info)
        try:
            non_participants_num=len(quiz_record_info['non_participants'])
        except:
            non_participants_num=0
        quiz.append({"cls":cls,"id":quiz_record.id,"generator":generator,"info":info,"subject":subject,"quiz":quiz_record.quiz,"non_participants_num":non_participants_num})
    #try:
        #quiz = user.quiz_set.all()
    #except:
        #return render(request, 'teacher/my_quizes.html')
    #quiz_dicts = list(quiz.values('id', 'info', 'subject', 'generator'))
    #for dic in quiz_dicts:
        #try:
            #dic['subject'] = Subject.objects.get(name=dic['subject']).chinese_name
            #dic['generator'] = user.username
            #dic['info']=json.loads(dic['info'])
       # except:
            #pass
    
    return render(request, 'quiz/my_quiz_records.html',{"quizInfo":quiz})

@login_required
def quiz_record(request):
    '''
    Only visited by teacher.
    See his or her quiz records.
    '''
    user=request.user
    if not user.groups.filter(name='TEACHER').exists():
        return render(request,'teacher/errorPage.html',{"errorType":"用户权限不足","particulars":"fault:user is not a teacher"})
    quiz_record_id=request.GET.get('quiz_record_id',"")
    try:
        quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
    except:
        return HttpResponse('quiz record not exist')
    generator = quiz_record.quiz.generator.username
    subject=Subject.objects.get(name=quiz_record.quiz.subject).chinese_name
    info = json.loads(quiz_record.quiz.info)
    cls = quiz_record.cls.name
    quiz_record_info=json.loads(quiz_record.info)
    try:
        non_participants=quiz_record_info['non_participants']
    except:
        non_participants=[]
    non_participants_num=len(non_participants)
    students=json.loads(quiz_record.cls.students)
    student_info=[]
    for student_id in students:
        if student_id in non_participants:
            status="未参加"
            time='——'
            score='——'
            rank='——'
        else:
            status="参加"
            try:
                student_quiz_record=StudentProfile.objects.get(quiz_record=quiz_record,student=student.user)
                time=student_quiz_record.datetime
            except:
                time='——'
        student = StudentProfile.objects.get(pk=student_id)
        try:
            score=quiz_record_info['student_marked'][str(student_profile.pk)]['score']
            rank=quiz_record_info['student_marked'][str(student_profile.pk)]['rank']
        except:
            score="——"
            rank="——"
        student_info.append({'id':student.pk,'student_no':student.student_no,'status':status,'time':time,'score':score,'name':student.name,'rank':rank})
    return render(request, 'quiz/quiz_record.html',{'students':student_info,'quiz_record_id':quiz_record_id,'cls':cls,'generator':generator,'subject':subject,'info':info,'non_participants_num':non_participants_num})

@staff_member_required
@csrf_exempt
def compose_quiz(request):
    if request.method == 'GET':
        subject = request.GET.get('subject', '')
        knowledge_node = request.GET.get('knowledge_node', '')

        f = QuestionQueryForm()
        
        if subject == '' and knowledge_node == '':
            return render(request, 'quiz/compose_quiz.html', {'form': f})
        
        if knowledge_node != '':
            try:
                node_object = KnowledgeNode.objects.get(id=knowledge_node)
            except:
                return HttpResponse('knowledge node does not exist')

            subject_object = node_object.graph.subject
        else:
            try:
                subject_object = Subject.objects.get(name=subject)
            except:
                return HttpResponse('subject does not exist')
        try:
            questions = Question.objects.filter(subject=subject_object)
        except:
            return HttpResponse('questions not found')
        if knowledge_node != '':
            questions = questions.filter(knowledge_node__id=knowledge_node)


        return render(request, 'quiz/compose_quiz.html', {'questions': questions, 'form': f})
    
    '''
    post data: subject, info, body, marking, public
    '''
    #posting
    subject = request.POST.get('subject', '')
    info = request.POST.get('info', '{}')
    body = request.POST.get('body', '')
    marking = request.POST.get('marking', '')
    public = request.POST.get('public', '')
    quiz_type = request.POST.get('quiz_type','')
    if not body:
        return HttpResponse('quiz body not found')

    if not subject:
        return HttpResponse('quiz subject not found')


    if marking == 'true':
        marking = True
    else:
        marking = False

    if public == 'true':
        public = True
    else:
        public = False

    try:
        quiz = Quiz(marking = marking, info = info, body = body, subject = subject, public = public,quiz_type=quiz_type,generator = request.user)
        #print(quiz)
        quiz.save()
    except Exception as e:
        #print(e)
        return HttpResponse('cannot create quiz')
    
    return HttpResponse(json.dumps({"status":"OK","quiz_id":quiz.id}))

@login_required
def questions_by_knowledge_node(request):
    pass

@login_required
def questions_page(request):
    if request.method != 'GET':
        return HttpResponse('wrong method')
    subject = request.GET.get('subject', '')
    knowledge_node = request.GET.get('knowledge_node', '')
    if subject == '' and knowledge_node == '':
        return render(request, 'quiz/questions.html')

    if knowledge_node != '':
        try:
            node_object = KnowledgeNode.objects.get(id=knowledge_node)
        except:
            return HttpResponse('knowledge node does not exist')

        subject_object = node_object.graph.subject
    
    else:
        try:
            subject_object = Subject.objects.get(name=subject)
        except:
            return HttpResponse('subject does not exist')

    try:
        questions = Question.objects.filter(subject=subject_object)
    except:
        return HttpResponse('questions not found')
    if knowledge_node != '':
        questions = questions.filter(knowledge_node__id=knowledge_node)

    return render(request, 'quiz/questions.html', {'questions': questions})
    

@login_required
def question_page(request):
    if request.method != 'GET':
        return HttpResponse('wrong method')

    question_id = request.GET.get('question_id', '')
    if question_id == '':
        return render(request, 'quiz/question.html')
    try:
        question = Question.objects.get(id=question_id)
    except:
        return HttpResponse('question not found')

    return render(request, 'quiz/question.html', {'question': question})

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        #fields = '__all__'
        exclude = ['knowledge_node']
        widgets = {
            'body': Textarea(attrs={'rows': '5', 'class': 'bg-light form-control', 'id': 'id_question_body'}),
            'subject': TextInput(attrs={'class': "bg-light form-control"}),
            #'knowledge_node': Select(attrs={'class': 'bg-light'}),
        }

class OptionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            order = kwargs.pop('order')
        except:
            order = None
        super(OptionForm, self).__init__(*args, **kwargs)
        if order:
            self.order_of_option = order
            for field in self.fields:
                #print(self.fields[field])
                self.fields[field].widget.attrs['id'] += '_' + str(order)
            
    class Meta:
        model = Option
        exclude = ['order', 'question', 'knowledge_node']
        widgets = {
            'body': Textarea(attrs={'rows': '5', 'class': 'bg-light form-control', 'id': 'id_option_body'}),
            #'order': TextInput(attrs={'id': 'id_option_order'}),
            #'question': Select(attrs={'id': 'id_option_question'}),
            'is_correct': CheckboxInput(attrs={'id': 'id_option_is_correct', 'class': 'bg-light form-control'}),
            'img': FileInput(attrs={'class': 'bg-light form-control', 'id': 'id_option_img'}),
            'error_reason': SelectMultiple(attrs={'class': 'bg-light form-control', 'id': 'id_option_error_reason'}),
            #'error_reason': MultipleChoiceField(),
            #'knowledge_node': TextInput(attrs={'id': 'id_option_knowledge_node'}),
        }

    

@staff_member_required
@csrf_exempt
def ajax_upload_question(request):
    user = request.user
    if request.method == 'GET':
        return HttpResponse('wrong method')

    question_id = request.POST.get('question_id', -1)
    if int(question_id) == -1:
        question_form = QuestionForm(request.POST)
    else:
        #print('old question')
        try:
            question = Question.objects.get(pk=question_id)
            question_form = QuestionForm(request.POST, instance=question)
        except:
            return HttpResponse('failed, question not existed') 

    img = request.FILES.get('img')
    if question_form.is_valid():
        try:
            q = question_form.save()
            q.knowledge_node = request.POST.getlist('nodes[]')
            # don't change uploader in amending.
            if int(question_id) == -1:
                q.uploader = user
            q.save()
            if img:
                q.img = img
                q.save()
        except Exception as e:
            return HttpResponse('failed')
    else:
        #print(question_form.errors)
        return HttpResponse('failed')
    return HttpResponse(q.id)

@staff_member_required
@csrf_exempt
def ajax_upload_option(request):
    if request.method == 'GET':
        return HttpResponse('wrong method')


    question_id = request.POST.get('question_id', -1)

    q = request.POST.get('question', '')
    if not q:
        return HttpResponse('no question')

    order = request.POST.get('order', '')
    if not order:
        return HttpResponse('no order')

    if int(question_id) == -1:
        option_form = OptionForm(request.POST)
    else:
        try:
            option = Option.objects.get(question__id=question_id, order=order)
            option_form = OptionForm(request.POST, instance=option)
            o = option_form.save()
            #print(2)
            
            error_reason = option_form.cleaned_data['error_reason']
            o.error_reason = error_reason
            
            knowledge_node = request.POST.getlist('nodes[]')
            o.knowledge_node = knowledge_node

            img = request.FILES.get('img')
            o.img = img
            o.save()
            #print(1)
            return HttpResponse('OK')
        except:
            return HttpResponse('failed, option not existed') 

    img = request.FILES.get('img')
    
    knowledge_node = request.POST.getlist('nodes[]')

    if option_form.is_valid():
        try:
            option_form.cleaned_data['question_id'] = q
            option_form.cleaned_data['order'] = order
            error_reason = option_form.cleaned_data['error_reason']
            option_form.cleaned_data.pop('error_reason')
            #print(option_form.cleaned_data)
            #print(error_reason)
            o = Option.objects.create(**option_form.cleaned_data)
            if error_reason:
                o.error_reason = error_reason
            if knowledge_node:
                o.knowledge_node = knowledge_node
            if img:
                o.img = img
            o.save()
        except Exception as e:
            #print(e)
            return HttpResponse('failed')
    else:
        #print(option_form.errors)
        return HttpResponse('failed')
    return HttpResponse('OK')

@login_required
def publish_quiz(request):
    if request.method == 'GET':
        return HttpResponse('wrong method')

    students = request.POST.get('students', '')
    classes = request.POST.get('classes', '')
    quiz_id = request.POST.get('quiz_id', '')
    
    if not quiz_id:
        return HttpResponse('not quiz id')

    try:
        quiz = Quiz.objects.get(quiz_id)
    except:
        return HttpResponse('quiz not exsited')

    #TODO: do we really need this now? push a quiz information to all students
    return HttpResponse('OK')

@csrf_exempt
@login_required
def mark_quiz(request):
    if request.method == 'GET':
        quiz_record_id = request.GET.get('quiz_record_id', '')
        if quiz_record_id == '':
            return render(request, 'quiz/mark_quiz.html')
        else:
            try:
                quiz_record=QuizRecord.objects.get(pk=quiz_record_id)
            except:
                return render(request,'teacher/errorPage.html',{"errorType":"参数数据错误","particulars":"fault:quizRecord not exsited"})
            user=request.user
            if user!=quiz_record.teacher.user:
                return render(request,'teacher/errorPage.html',{"errorType":"该用户没有此测评","particulars":"fault:user not having quizRecord"})
            quiz=quiz_record.quiz
            cls=quiz_record.cls.name
            try:
                title=json.loads(quiz.info)['title']
            except:
                pass
            quiz_body = json.loads(quiz.body)
            quiz_body_key_int=[]
            for key in quiz_body:
                quiz_body_key_int.append(int(key))
            quiz_body_key_int.sort()
            questions =[]
            questions_json=[]
            #print(quiz_body)
            for body in quiz_body_key_int:
                #print(body)
                try:
                    question = Question.objects.get(pk = quiz_body[str(body)][0])
                    #print(str(question.img))
                    question_info={"body":question.body,"image":question.img.name,"score":quiz_body[str(body)][1],"order":body}
                    question_info_json={"body":question.body,"score":quiz_body[str(body)][1],"order":body}
                except:
                    return render(request,'teacher/errorPage.html',{"errorType":"数据紊乱","particulars":"fault:question not exsited"})
                try:
                    options = question.options.all().order_by('order')
                except:
                    return render(request,'teacher/errorPage.html',{"errorType":"数据紊乱","particulars":"fault:option not exsited"})
                options_dicts = list(options.values('body','order','img','is_correct'))
                option_dicts=[]
                for option in  options_dicts:
                    option_dicts.append({"body":option["body"],"order":option["order"],"image":option["img"],"is_correct":option["is_correct"]})
                knowledge_node = KnowledgeNode.objects.filter(question=question)
                knowledge_nodes = []
                for kn in knowledge_node:
                    knowledge_nodes.append(kn.title)
                questions.append({"question_id":question.id,"question":question_info,"options":option_dicts,"knowledge_nodes":knowledge_nodes})
                questions_json.append({"question_id":question.id,"question":question_info_json,"options":option_dicts})
            quiz_info={"cls":cls,"title":title,"quizRecordId":quiz_record_id,"questions":questions}
            #print(quiz_info)
            json_data=json.dumps({"cls":cls,"title":title,"quizRecordId":quiz_record_id,"questions":questions_json})
            #print(json_data)
            return render(request, 'quiz/mark_quiz.html', {'quizInfo': quiz_info, 'json_data':json_data})
    
    '''
    #POST
    accepting data
    generate student quiz record
    update whole quiz record
    generate report
    '''
    request_dic = json.loads(request.body.decode('utf-8'))
    #print(request_dic)
    #student_id = request.POST.get('student_id', '')
    try:
        student_id = request_dic['studentId']
    except:
        return HttpResponse('no student id')
    
    try:
        student_profile = StudentProfile.objects.get(student_no=student_id)
    except:
        return HttpResponse('student not existed')
    #TODO: check plan
    
    #quiz_id = request.POST.get('quiz_record_id', '')
    try:
        quiz_record_id = request_dic['quizRecordId']
    except:
        return HttpResponse('no quiz record id')

    try:
        quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
    except:
        return HttpResponse('quiz record not existed')

    try:
        answer_dic = json.loads(request_dic['questionAndAnswer'])
    except:
        return HttpResponse('no answers')
    
    #print(answer_dic)
    tmp = answers_to_nodes(answer_dic)
    if tmp['status'] == False:
        return HttpResponse('failed: ' + tmp['reason'])

    score_dic = tmp['data']
    nodes_dic = tmp['nodes_dic']
    #print(nodes_dic)

    # XXX: algo 101, pure stats
    update_nodes(student_profile.student_no, score_dic)

    quiz_data = mark_quiz_wrapper(student_id, quiz_record_id, answer_dic)
    #print(quiz_data)
    #return HttpResponse(200)

    # TODO: create student quiz record
    # TODO: update quiz_record

    # zhijie
    dic1 = {}
    quiz=quiz_record.quiz
    dic1['studentName']=student_profile.name
    dic1['title']=json.loads(quiz.info)['title']
    dic1['studentId']=str(student_profile.pk)
    dic1['quizId']=str(quiz.pk)
    dic1['time']=quiz_record.datetime.strftime('%Y-%m-%d')
    dic1['schoolName']=quiz_record.cls.school.name
    try:
        subject=Subject.objects.get(pk=quiz.subject)
    except:
        return HttpResponse('subject not existed')
    dic1['subject']=subject.chinese_name
    dic1['subject_id']=subject.name
    #print(quiz.info)
    try:
        questionNum=json.loads(quiz.info)['question_num']
    except:
        questionNum=''
    try:
        totalPoint=json.loads(quiz.info)['total_point']
    except:
        totalPoint = ''
    try:
        difficulty=json.loads(quiz.info)['difficulty']
    except:
        difficulty=''
    dic1['quizInfo']={"questionNum":questionNum,"totalPoint":totalPoint,"difficulty":difficulty}
    try:
        quiz_record_info = json.loads(quiz_record.info)
        #print(quiz_record_info)
        ranking=quiz_record_info['student_marked'][str(student_profile.pk)]['rank']
        dic1['score']=quiz_record_info['student_marked'][str(student_profile.pk)]['score']
        dic1['quizRecordInfo']={"average":quiz_record_info["averageScore"],"topScore":quiz_record_info['topScore'],"lowestScore":quiz_record_info['lowestScore'],"ranking":ranking}
    except:
        dic1['score']=''
        dic1['quizRecordInfo']={}
    quiz_records=QuizRecord.objects.filter(cls=quiz_record.cls)



    if quiz.quiz_type == 'small':
        questions = []
        question_ids = map(lambda x: x[0], json.loads(quiz.body).values())
        quiz_questions = Question.objects.filter(pk__in=question_ids)
        for question in quiz_questions:
            question_dic = {}
            question_dic['id'] = question.pk
            question_dic['question'] = question.body
            question_dic['option'] = []
            if question.img:
                question_dic['image'] = question.img.url
            question_dic['analysis'] = question.analysis
            for option in question.options.all():
                option_dic = {"order": option.order, "body": option.body}
                if option.img:
                    option_dic['image'] = option.img.url
                question_dic['option'].append(option_dic)
                if option.is_correct:
                    question_dic['answer'] = option.order

            questions.append(question_dic)

        dic1['questions'] = questions

    else:
        #print(quiz_records)
        student_quiz_record=list(StudentQuizRecord.objects.filter(student=student_profile.user,quiz_record__in=quiz_records).order_by("-datetime").values("datetime","score"))
        #print(len(student_quiz_record))
        if len(student_quiz_record)>8:
            student_quiz_record=student_quiz_record[0:8]

        score=[]
        time=[]
        for index in student_quiz_record:
            score.append(index['score'])
            time.append(index['datetime'].strftime('%Y-%m-%d'))
        dic1['image2']={"x":time,"y1":score}

    # score=[]
    # time=[]
    # for index in student_quiz_record:
    #     score.append(index['score'])
    #     time.append(index['datetime'].strftime('%Y-%m-%d'))
    # dic1['image2']={"x":time,"y1":score}
    #print(dic1)

    # xu
    dic2 = {}
    # knowledgeAnalysis
    knowledgeAnalysis = {'subject': subject.chinese_name}
    node_pks = nodes_dic.keys()
    nodes_vector = get_node_scores(student_id, node_pks)
    #print(nodes_vector)

    knowledges = []

    for node_pk in nodes_vector:
        try:
            node = KnowledgeNode.objects.get(pk=node_pk)
        except:
            continue
        tmp = {}
        tmp['knowledgeNode'] = node.title
        tmp['knowledgeGraph'] = node.graph.description

        #FIXME: difficulty doesn't have a meanning at this moment
        tmp['difficulty'] = 0
        tmp['scoreRatio'] = round(nodes_dic[node_pk]['correct']/nodes_dic[node_pk]['count'], 2) * 100
        #tmp['scoreRatio'] = 60 + nodes_vector[node_pk]['score'] * 10
        #if tmp['scoreRatio'] >= 100:
        #    tmp['scoreRation'] = 100
        tmp['score'] = round(nodes_vector[node_pk]['score'], 1)

        knowledges.append(tmp)

    errorReason = quiz_data['error_reasons']

    knowledgeAnalysis['knowledges'] = knowledges
    knowledgeAnalysis['errorReason'] = errorReason

    # upScoreStrategy
    upScoreStrategy = {}
    upScore = 0
    knowledges = []
    for node_pk in nodes_vector:
        if nodes_vector[node_pk]['score'] < 0.5:
            dic = get_predecessors(node_pk)
            tmp = {}
            try:
                node = KnowledgeNode.objects.get(pk=node_pk)
            except:
                continue
            tmp['knowledgeNode'] = node.title
            tmp['masteryDegree'] = round(nodes_vector[node_pk]['score'], 1) * 5
            # TODO: what should be done here?
            tmp['advancement'] = round((0.8 - nodes_vector[node_pk]['score']) * 5, 1)
            upScore += tmp['advancement']
            tmp['strengthenKnowledge'] = []

            if dic['status'] == True:
                predecessor_pks = dic['nodes']

                related_node_scores = get_node_scores(student_id, predecessor_pks)
                for node_pk in related_node_scores:
                    if related_node_scores[node_pk]['score'] < 0.6:
                        try:
                            node = KnowledgeNode.objects.get(pk=node_pk)
                        except:
                            continue

                        tmp['strengthenKnowledge'].append(node.title)
            knowledges.append(tmp)

    upScoreStrategy['upScore'] = round(upScore, 1)
    upScoreStrategy['knowledges'] = knowledges

            

                        
    #print(related_node_scores)
    '''
    for node_pk in related_node_scores:
        if related_node_scores[node_pk] >= 0.5:
            try:
                node = KnowledgeNode.objects.get(pk=node_pk)
            except:
                pass
                tmp = {}
                tmp['knowledgeNode'] = node.title
                tmp['masteryDegree'] = related_node_scores[node_pk]
                # FIXME: what should be done here?
                tmp['advancement'] = (0.8 - related_node_scores[node_pk]) * 5

    '''
    
    # learningArchives
    learningArchives = {}
    detail = []
    node_names = []

    graph_pks = KnowledgeNode.objects.filter(pk__in=node_pks).values_list('graph__pk', flat=True)
    for graph_pk in graph_pks:
        graph_node_vector = get_or_create_graph_vector(student_id, graph_pk)
        graph_node_vector=json.loads(graph_node_vector)
        if graph_node_vector['status'] != 'success':
            continue
        graph_node_vector = graph_node_vector['data']
        for node_id in graph_node_vector:
            try:
                node = KnowledgeNode.objects.get(pk=node_id)
            except:
                continue
            if node.title in node_names:
                continue
            if graph_node_vector[node_id]['belief'] == 1:
                continue
            detail.append({'knowledge_node': node.title, 'masteryDegree': round(graph_node_vector[node_id]['score'], 1)})
            node_names.append(node.title)

    learningArchives['detail'] = detail

    # image1
    image1 = {}
    # vals2 means portion of nodes
    vals2 = []
    vals1 = []
    labels = []
    for node_id in nodes_dic:
        try:
            node = KnowledgeNode.objects.get(pk = node_id)
        except:
            continue
        labels.append(node.title)
        vals2.append(round(nodes_dic[node_id]['count'], 1))
        vals1.append(round(score_dic[node_id], 1))

    image1['vals2'] = vals2
    image1['vals1'] = vals1
    image1['labels'] = labels

    dic2['knowledgeAnalysis']=knowledgeAnalysis
    dic2['upScoreStrategy']=upScoreStrategy
    dic2['learningArchives']=learningArchives
    dic2['image1']=image1
    #print(dic2['learningArchives'])
    #print(dic2)
    dic1.update(dic2)
    data=json.dumps(dic1)
    #print(dic1)
    headers={"Content-Type":"application/json"}
    if quiz.quiz_type == 'full':
        requests.post(url='http://47.110.253.251' + '/templates/quizReport/' + 'pdf',data=data,headers=headers)
        requests.post(url='http://47.110.253.251' + '/templates/quizReport/' + 'html',data=data,headers=headers)
    else:
        requests.post(url='http://47.110.253.251' + '/templates/classQuizReport/' + 'pdf',data=data,headers=headers)
        requests.post(url='http://47.110.253.251' + '/templates/classQuizReport/' + 'html',data=data,headers=headers)
        
    d = {'isFinish': True}
    return HttpResponse(json.dumps(d))

@login_required
def ajax_get_questions(request):
    chapter_id = request.GET.get('chapter_id', '')
    question_id=request.GET.get('questionId','')
    subject = request.GET.get('subject', '')
    node_id = request.GET.get('node_id', '')
    page = request.GET.get('page', '1')
    date = request.GET.get('date', '')
    node=request.GET.get('node','true')
    # FIXME: this could be very slow
    questions = Question.objects.all()
    if date:
        datetime = date.split('-')
        questions = questions.filter(datetime__year=datetime[0],datetime__month=datetime[1],datetime__day=datetime[2])
    if subject:
        questions = questions.filter(subject=subject)
    if node_id:
        node = KnowledgeNode.objects.get(id=node_id)
        questions = questions.filter(knowledge_node=node)
    if question_id:
        try:
            questions = Question.objects.filter(pk=question_id)
        except:
            return HttpResponse('missing question_id')
    if node=='false':
        questions=questions.filter(knowledge_node=None)
        
    page = int(page)
    paginator = Paginator(questions, 25)
    try:
        questions = paginator.page(page)
    except:
        #questions = paginator.page(1)
        return HttpResponse('error')
    d = {}
    for question in questions:
        val = {}
        val['body'] = question.body
        val['analysis'] = question.analysis
        if question.img:
            val['img_url'] = question.img.url
        options = {}
        for option in question.options.all():
            option_dic = {}
            option_dic['body'] = option.body
            option_dic['id'] = option.id
            if option.img:
                option_dic['img_url'] = option.img.url
            options[option.order] = option_dic
        val['options'] = options
        d[question.id] = val
    return HttpResponse(json.dumps(d))

def ajax_get_own_question_by_id(request):
    question_id=request.GET.get('questionId','')
    subject = request.GET.get('subject', '')
    node_id = request.GET.get('node_id', '')
    page = request.GET.get('page', '1')
    date = request.GET.get('date', '')
    node = request.GET.get('node','true')
    user = request.user
    questions = user.questions_uploaded.all().order_by('-id')
    if date:
        datetime = date.split('-')
        questions = questions.filter(datetime__year=datetime[0],datetime__month=datetime[1],datetime__day=datetime[2])
    if subject:
        questions = questions.filter(subject=subject)
    if node_id:
        node = KnowledgeNode.objects.get(id=node_id)
        questions = questions.filter(knowledge_node=node)
    if question_id:
        try:
            questions = Question.objects.filter(pk=question_id)
        except:
            return HttpResponse('missing question_id')
    if node=='false':
        questions = questions.filter(knowledge_node=None)
    #else:
        #if not subject and not node_id:
            #return HttpResponse('missing subject and node_id')
        #if not subject:
            #try:
                #node = KnowledgeNode.objects.get(id=node_id)
            #except:
                #return HttpResponse('knowledge node not existed', status=400)
            #subject = node.graph.subject
        #questions = questions.filter(subject=subject)
        #if node_id:
            #try:
                #node = KnowledgeNode.objects.get(id=node_id)
            #except:
                #return HttpResponse('knowledge node not existed', status=400)
            #questions = questions.filter(knowledge_node=node)
        #if date:
            #datetime=date.split('-')
            #questions = questions.filter(datetime__year=datetime[0],datetime__month=datetime[1],datetime__day=datetime[2])
    page = int(page)
    paginator = Paginator(questions, 25)
    try:
        questions = paginator.page(page)
    except:
        #questions = paginator.page(1)
        return HttpResponse('error')
    d = {}
    for question in questions:
        val = {}
        val['body'] = question.body
        val['analysis'] = question.analysis
        if question.img:
            val['img_url'] = question.img.url
        options = {}
        for option in question.options.all():
            option_dic = {}
            option_dic['body'] = option.body
            option_dic['id'] = option.id
            if option.img:
                option_dic['img_url'] = option.img.url
            options[option.order] = option_dic
        val['options'] = options
        d[question.id] = val
    return HttpResponse(json.dumps(d))

@login_required
@csrf_exempt
def ajax_delete_question(request):
    question_id=request.GET.get("question_id","")
    if question_id=='':
        return HttpResponse('failed: missing field question id')
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return HttpResponse('question not existed')
    try:
        question.delete()
    except:
        return HttpResponse('question not delete')
    return HttpResponse('OK')

@login_required
def upload_question(request):
    question_id = request.GET.get('question_id', '')
    if question_id:
        try:
            q = Question.objects.get(pk=question_id)
        except:
            return HttpResponse('question not exited')

        question_form = QuestionForm(instance=q)
        option_forms = []
        knowledge_nodes = list(q.knowledge_node.all().values_list('id', 'description'))

        knowledge_nodes = [list(map(str, l)) for l in knowledge_nodes]
        
        nodes_arrs = {}
        nodes_id_arrs = {}

        for o in q.options.all().order_by('order'):
            option_forms.append(OptionForm(instance=o, order=o.order))
            nodes_arrs[str(o.order)] = [list(map(str, l)) for l in list(o.knowledge_node.all().values_list('id', 'description'))]
            nodes_id_arrs[str(o.order)] = [str(s) for s in o.knowledge_node.all().values_list('id', flat=True)]
        #print(question_form) 
        return render(request, 'quiz/upload_question.html', {'knowledge_nodes': knowledge_nodes, 'nodes_arrs': nodes_arrs, 'nodes_id_arrs': nodes_id_arrs, 'question_id':question_id, 'question_form': question_form, 'option_forms': option_forms})
            
        
    else:
        question_form = QuestionForm()
        option_forms = []
        option_forms.append(OptionForm(order='A'))
        option_forms.append(OptionForm(order='B'))
        option_forms.append(OptionForm(order='C'))
        option_forms.append(OptionForm(order='D'))
        return render(request, 'quiz/upload_question.html', {'nodes_arrs': None, 'question_form': question_form, 'option_forms': option_forms})

@login_required
def upload_quiz_question_answer(request):
    if request.method == 'GET':
        #TODO: redirect to upload answer
        return HttpResponse('OK')

    quiz_id = request.POST.get('quiz_id', '')
    question_id = request.POST.get('question_id', '')
    option = request.POST.get('option', '')
    student_id = request.POST.get('student_id', '')

    # terminator
    if question_id == 'done':
        return HttpRespone('quiz upload is finished')
    else:
        #TODO:
        '''
            get quiz, get question, get student, get option
        '''
        #TODO: get to next question
        return HttpResponse('go to next question')
    

@login_required
def get_next_question(request):
    user = request.user
    if not user.groups.filter(name='STUDENT').exists():
        return HttpResponse('failed: user is not a student')

    subject = request.GET.get('subject', '')
    if not subject:
        return HttpResponse('failed: no subject')
    
    questions = Question.objects.filter(subject = subject)

    if len(questions) == 0:
        return HttpResponse('failed: no question available')

    #TODO: add an algo
    return HttpResponse(questions[int(len(questions)/2)].pk)

@login_required
def upload_quiz_answer_sheet(request):
    if request.method == 'GET':
        #TODO: redirect to direct upload
        
        return HttpResponse('OK')

    answer_sheet = request.POST.get('answer_sheet', '')
    try:
        answers = json.loads(answer_sheet)
    except:
        return HttpResponse('wrong format')

    nodes_dic = mark_quiz(answers) 
    return HttpResponse('OK')

@login_required
def ajax_get_own_questions(request):
    user = request.user
    questions = user.questions_uploaded.all().order_by('-id')
    #questions = user.questions_uploaded.all()
    
    l = []
    d = {}
    for question in questions:
        val = {}
        val['body'] = question.body
        if question.analysis:
            val['analysis'] = question.analysis
        if question.img:
            #print(question.img.url)
            val['img_url'] = question.img.url
        options = {}
        for option in question.options.all():
            option_dic = {}
            option_dic['body'] = option.body
            option_dic['id'] = option.id
            if option.img:
                option_dic['img_url'] = option.img.url
            options[option.order] = option_dic
        val['options'] = options
        d[question.id] = val
        l.append([question.id, val])
    
    return HttpResponse(json.dumps(l))
    return HttpResponse(json.dumps(d))

@login_required
@csrf_exempt
def mark_question(request):
    if request.method == 'GET':
        return HttpResponse('wrong method')
    d = json.loads(request.body.decode('utf-8'))
    error = {}
    error['result'] = True
    error['reason'] = ''
    try:
        student_id = d['studentId']
        question_id = d['questionId']
        option_answer = d['optionAnswer']
    except:
        #failed
        error['reason'] = 'missing field'
        return HttpResponse(json.dumps(error))

    try:
        question = Question.objects.get(pk=question_id)
    except:
        # question not existed
        error['reason'] = 'question not existed'
        return HttpResponse(json.dumps(error))

    res = {}
    #TODO:update vector
    for option in question.options.all():
        if option.is_correct:
            res['rightAnswers'] = option.order
        if option.order == option_answer:
            if option.error_reason:
                res['errorReason'] = list(option.error_reason.all().values_list('description', flat=True))
            else:
                res['errorReason'] = []
    
    if question.analysis:
        res['answerAnalysis'] = question.analysis
    else:
        res['answerAnalysis'] = ''

    res['analysis'] = ''



    return HttpResponse(json.dumps(res))

    
@login_required
@csrf_exempt
def add_question_to_favorites(request):
    if request.method == 'GET':
        return HttpResponse('wrong method, should be POST')

    user = request.user
    if not user.groups.filter(name='TEACHER').exists():
        return HttpResponse('user is not a teacher')
    
    dic = json.loads(request.body.decode('utf-8'))
    try:
        question_id = dic['question_id']
    except:
        return HttpResponse('failed: missing field question id')

    try:
        question = Question.objects.get(pk=question_id)
    except:
        return HttpResponse('question not existed')

    try:
        f = user.teacherprofile.favorites
        f.questions.add(question)
        f.save()
    except:
        return HttpResponse('question adding to favorites failed')

    return HttpResponse('OK')
@login_required
@csrf_exempt
def ajax_save_quiz_record(request):
    user=request.user
    if request.method == "POST":
        quiz_id=request.POST.get("quiz_id",'')
        cls_id=request.POST.get('cls_id','')
        try:
            quiz=Quiz.objects.get(pk=quiz_id)
        except:
            return HttpResponse("quiz not having")
        try:
            cls=Cls.objects.get(pk=cls_id)
        except:
            return HttpResponse('class not having')
        if cls.teacher.user!=user:
            return HttpResponse("user not having this class")
        if QuizRecord.objects.filter(quiz_id=quiz_id,cls_id=cls_id).exists():
            return HttpResponse('quiz record is having')
        info=json.dumps({'non_participants':json.loads(cls.students)})
        quiz_record=QuizRecord(info=info,quiz=quiz,teacher=user.teacherprofile,cls=cls,datetime=datetime.datetime.now())
        try:
            quiz_record.save()
        except:
            return HttpResponse("save failed")
        return HttpResponse("OK")
    return HttpResponse("method error")
@login_required
@csrf_exempt
def ajax_save_quiz_and_publish(request):
    user=request.user
    subject_id = request.POST.get('subject', '')
    info = request.POST.get('info', '{}')
    body = request.POST.get('body', '')
    marking = request.POST.get('marking', '')
    public = request.POST.get('public', '')
    quiz_type = request.POST.get('quiz_type','')
    cls_id=request.POST.get('cls_id','')
    if not body:
        return HttpResponse('quiz body not found')
    if marking == 'true':
        marking = True
    else:
        marking = False
    if public == 'true':
        public = True
    else:
        public = False
    try:
        cls=Cls.objects.get(pk=cls_id)
    except:
        return HttpResponse('class not having')
    if cls.teacher.user!=user:
        return HttpResponse("user not having this class")
    try:
        subject = Subject.objects.get(pk=subject_id)
    except:
        return HttpResponse('subject not found')
    if cls.subject!=subject_id:
        return HttpResponse("class subject is not quiz subject")
    try:
        quiz = Quiz(marking = marking, info = info, body = body, subject = subject, public = public,quiz_type=quiz_type,generator = request.user)
        quiz.save()
    except Exception as e:
        return HttpResponse('cannot create quiz')
    info=json.dumps({'non_participants':json.loads(cls.students)})
    quiz_record=QuizRecord(info=info,quiz=quiz,teacher=user.teacherprofile,cls=cls,datetime=datetime.datetime.now())
    try:
        quiz_record.save()
    except:
        return HttpResponse("save failed")
    return HttpResponse(json.dumps({"title":json.loads(quiz.info)['title'],"quiz_id":quiz.id,"id":quiz_record.id,"cls":cls.name,"subject":subject.chinese_name}))


@login_required
def ajax_get_page_count_by_section(request):
    section_id = request.GET.get('section_id', '')
    selected = request.GET.get('selected','')
    if not section_id:
        return HttpResponse('failed: section_id missing')
    try:
        section = Section.objects.get(pk=section_id)
    except:
        return HttpResponse('failed: section not found with this id')

    questions = Question.objects.filter(knowledge_node__in=json.loads(section.nodes_list))
    if selected=="true":
        questions = questions.filter(selected=True)
    return HttpResponse(int((len(questions.all()) + 24)/25))

@login_required
def ajax_get_questions_by_section(request):
    section_id = request.GET.get('section_id', '')
    page = request.GET.get('page', '1')
    selected = request.GET.get('selected','')
    page = int(page)

    if not section_id:
        return HttpResponse('failed: section_id missing')
    try:
        section = Section.objects.get(pk=section_id)
    except:
        return HttpResponse('failed: section not found with this id')

    questions = Question.objects.filter(knowledge_node__in=json.loads(section.nodes_list))
    if selected=="true":
        questions = questions.filter(selected=True)
    page = int(page)
    
    paginator = Paginator(questions, 25)

    try:
        questions = paginator.page(page)
    except:
        questions = paginator.page(1)

    d = {}
    for question in questions:
        val = {}
        val['body'] = question.body
        if question.img:
            val['img_url'] = question.img.url
        options = {}
        for option in question.options.all():
            option_dic = {}
            option_dic['body'] = option.body
            option_dic['id'] = option.id
            if option.img:
                option_dic['img_url'] = option.img.url
            options[option.order] = option_dic
        val['options'] = options
        d[question.id] = val

    return HttpResponse(json.dumps(d))

@login_required
def ajax_get_questions_by_node(request):
    return HttpResponse('OK')


@staff_member_required
def compose_quizs(request):
    if request.method == 'GET':
        user=request.user
        school=TeacherProfile.objects.get(user=user).school.name
        subject = request.GET.get('subject', '')
        knowledge_node = request.GET.get('knowledge_node', '')

        f = QuestionQueryForm()
        if subject == '' and knowledge_node == '':
            return render(request, 'quiz/compose_quizs.html', {'form': f,'school':school})

        if knowledge_node != '':
            try:
                node_object = KnowledgeNode.objects.get(id=knowledge_node)
            except:
                return HttpResponse('knowledge node does not exist')

            subject_object = node_object.graph.subject
        else:
            try:
                subject_object = Subject.objects.get(name=subject)
            except:
                return HttpResponse('subject does not exist')
        try:
            questions = Question.objects.filter(subject=subject_object)
        except:
            return HttpResponse('questions not found')
        if knowledge_node != '':
            questions = questions.filter(knowledge_node__id=knowledge_node)
        return render(request, 'quiz/compose_quizs.html', {'questions': questions, 'form': f,'school':school})

    '''
    post data: subject, info, body, marking, public
    '''
    # posting
    subject = request.POST.get('subject', '')
    info = request.POST.get('info', '{}')
    body = request.POST.get('body', '')
    marking = request.POST.get('marking', '')
    public = request.POST.get('public', '')

    if not body:
        return HttpResponse('quiz body not found')

    if not subject:
        return HttpResponse('quiz subject not found')

    if marking == 'true':
        marking = True
    else:
        marking = False

    if public == 'true':
        public = True
    else:
        public = False

    try:
        quiz = Quiz(marking=marking, info=info, body=body, subject=subject, public=public, generator=request.user)
        # print(quiz)
        quiz.save()
    except Exception as e:
        # print(e)
        return HttpResponse('cannot create quiz')

    return HttpResponse('OK')

@login_required
def ajax_get_page_count_by_chapter(request):
    chapter_id = request.GET.get('chapter_id', '')
    selected = request.GET.get('selected','')
    if not chapter_id:
        return HttpResponse('failed: chapter_id missing')
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
    except:
        return HttpResponse('failed: chapter not found with this id')

    nodes_list = []
    for section in chapter.sections.all():
        nodes_list += json.loads(section.nodes_list)
    nodes_list = list(set(nodes_list))

    questions = Question.objects.filter(knowledge_node__in=nodes_list)
    if selected=="true":
        questions = questions.filter(selected=True)
    return HttpResponse(int((len(questions.all()) + 24)/25))

@login_required
def ajax_get_questions_by_chapter(request):
    chapter_id = request.GET.get('chapter_id', '')
    page = request.GET.get('page', '1')
    selected = request.GET.get('selected','')
    page = int(page)

    if not chapter_id:
        return HttpResponse('failed: chapter_id missing')
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
    except:
        return HttpResponse('failed: chapter not found with this id')

    nodes_list = []
    for section in chapter.sections.all():
        nodes_list += json.loads(section.nodes_list)

    nodes_list = list(set(nodes_list))

    questions = Question.objects.filter(knowledge_node__in=nodes_list)

    if selected=="true":
        questions = questions.filter(selected=True)
    page = int(page)
    
    paginator = Paginator(questions, 25)

    try:
        questions = paginator.page(page)
    except:
        questions = paginator.page(1)

    d = {}
    for question in questions:
        val = {}
        val['body'] = question.body
        if question.img:
            val['img_url'] = question.img.url
        options = {}
        for option in question.options.all():
            option_dic = {}
            option_dic['body'] = option.body
            option_dic['id'] = option.id
            if option.img:
                option_dic['img_url'] = option.img.url
            options[option.order] = option_dic
        val['options'] = options
        d[question.id] = val

    return HttpResponse(json.dumps(d))

