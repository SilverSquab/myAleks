#coding=utf-8
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
from django import forms

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
        return HttpResponse('wrong method')
    quiz_id = request.GET.get('quizId','')
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except:
        return HttpResponse('quiz not exsited')
    quiz.subject = Subject.objects.get(name=quiz.subject).chinese_name
    quiz.info=json.loads(quiz.info)

    #print(quiz)
    quiz_body = json.loads(quiz.body)
    questions =[]
    #print(quiz_body)
    for body in quiz_body:
        print(quiz_body[body][0])
        try:
            question = Question.objects.get(pk = quiz_body[body][0])
        except:
            return HttpResponse('question ont exsited')
        options = question.options.all()
        options_dicts = list(options.values('body','order','img'))
        questions.append({'question':question,'options':options})
    return render(request, 'quiz/quiz_detail.html',{"quizInfo":quiz,'questions':questions})

@login_required
def quiz_records(request):
    '''
    Only visited by teacher.
    See his or her quiz records.
    '''
    return render(request, 'quiz/my_quiz_records.html')

@login_required
def quiz_record(request):
    '''
    Only visited by teacher.
    See his or her quiz records.
    '''
    return render(request, 'quiz/quiz_record.html')

@staff_member_required
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
        quiz = Quiz(marking = marking, info = info, body = body, subject = subject, public = public, generator = request.user)
        #print(quiz)
        quiz.save()
    except Exception as e:
        #print(e)
        return HttpResponse('cannot create quiz')


    return HttpResponse('OK')

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
        quiz_id = request.GET.get('quiz_id', '')
        if quiz_id == '':
            return render(request, 'quiz/mark_quiz.html')
        else:
            test_data = '{"cls": "\\u9ad8\\u4e09\\u5730\\u7406", "questions": [{"knowledge_nodes": ["node1", "node2"], "question": {"body": "\\u4ee5\\u4e0b\\u5730\\u7406\\u73b0\\u8c61\\u4e2d\\uff0c\\u4e0d\\u662f\\u7531\\u4e8e\\u5730\\u7403\\u81ea\\u8f6c\\u4ea7\\u751f\\u7684\\u662f(    )", "image": "", "score": 2, "order": "2"}, "options": [{"body": "\\u663c\\u591c\\u73b0\\u8c61", "is_correct": "False", "image": "", "order": "A"}, {"body": "\\u663c\\u591c\\u4ea4\\u66ff\\u73b0\\u8c61", "is_correct": "False", "image": "", "order": "B"}, {"body": "\\u65f6\\u5dee\\u7684\\u4ea7\\u751f", "is_correct": "False", "image": "", "order": "C"}, {"body": "\\u5730\\u8868\\u6c34\\u5e73\\u8fd0\\u52a8\\u7684\\u7269\\u4f53\\u65b9\\u5411\\u53d1\\u751f\\u504f\\u8f6c", "is_correct": "True", "image": "", "order": "D"}], "question_id": 102}, {"knowledge_nodes": ["node1", "node2"], "question": {"body": "\\u5317\\u4eac\\u65f6\\u95f42010\\u5e7410\\u67081\\u65e518\\u65f659\\u520657\\u79d2\\uff0c\\u201c\\u5ae6\\u5a25\\u4e8c\\u53f7\\u201d\\u63a2\\u6708\\u536b\\u661f\\u6210\\u529f\\u53d1\\u5c04\\uff0c\\u4f4d\\u4e8e\\u592a\\u5e73\\u6d0b\\u4e0a\\u7684\\u8fdc\\u671b\\u4e94\\u53f7\\u6d4b\\u91cf\\u8239\\uff08\\u7ea6150\\u00b0E\\uff09\\u5bf9\\u5176\\u8fdb\\u884c\\u540c\\u6b65\\u76d1\\u6d4b\\u3002\\u636e\\u6b64\\u5b8c\\u62101\\uff5e3\\u9898\\u3002\\r\\n3\\uff0e\\u4e0e\\u6708\\u7403\\u76f8\\u6bd4\\uff0c\\u5730\\u7403\\u7684\\u7279\\u6b8a\\u6027\\u5728\\u4e8e", "image": "", "score": 2, "order": "1"}, "options": [{"body": "\\u663c\\u591c\\u73b0\\u8c61", "is_correct": "False", "image": "", "order": "A"}, {"body": "\\u663c\\u591c\\u4ea4\\u66ff\\u73b0\\u8c61", "is_correct": "False", "image": "", "order": "B"}, {"body": "\\u65f6\\u5dee\\u7684\\u4ea7\\u751f", "is_correct": "False", "image": "", "order": "C"}, {"body": "\\u5730\\u8868\\u6c34\\u5e73\\u8fd0\\u52a8\\u7684\\u7269\\u4f53\\u65b9\\u5411\\u53d1\\u751f\\u504f\\u8f6c", "is_correct": "True", "image": "", "order": "D"}], "question_id": 103}], "quizRecordId": "1", "title": "4\\u670815\\u65e5\\u5730\\u7406\\u7b2c\\u4e00\\u6b21\\u8003\\u8bd5"}'
            quiz_info = json.loads(test_data)
            json_data = json.dumps(quiz_info)
            #print(json_data)
            return render(request, 'quiz/mark_quiz.html', {'quizInfo': quiz_info, 'json_data': json_data})

    request_dic = json.loads(request.body.decode('utf-8'))
    

    #student_id = request.POST.get('student_id', '')
    try:
        student_id = request_dic['studentId']
    except:
        return HttpResponse('no student id')
    
    try:
        student = User.objects.get(pk=student_id)
    except:
        return HttpResponse('student not existed')
    #TODO: check if user is in student group
    #TODO: check plan
    
    #quiz_id = request.POST.get('quiz_record_id', '')
    try:
        quiz_record_id = request_dic['quizRecordId']
    except:
        return HttpResponse('no quiz record id')

    try:
        quiz = Quiz.objects.get(pk=quiz_record_id)
    except:
        return HttpResponse('quiz record not existed')

    try:
        answer_dic = request_dic['questionAndAnswer']
    except:
        return HttpResponse('no answers')

    #TODO: mark this quiz for this student
    d = {'isFinish': True}
    return HttpResponse(json.dumps(d))


@login_required
def ajax_get_questions(request):
    #print(request.GET)
    subject = request.GET.get('subject', '')
    node_id = request.GET.get('node_id', '')
    page = request.GET.get('page', '1')
    date = request.GET.get('date', '')
    if not subject and not node_id:
        #print(1)
        return HttpResponse('missing subject and node_id')

    if not subject:
        try: 
            node = KnowledgeNode.objects.get(id=node_id)
        except:
            return HttpResponse('knowledge node not existed', status=400)

        subject = node.graph.subject
        #print(subject)

    #print(date)
    #print(type(date))
    

    #try:
    #    subject = Subject.objects.get(name=subject_str)
    
    #except:
    #    return HttpResponse('subject not existed')

    questions = Question.objects.filter(subject=subject)
    #print(len(questions))

    if node_id:
        try:
            node = KnowledgeNode.objects.get(id=node_id)
        except:
            return HttpResponse('knowledge node not existed', status=400)
        questions = questions.filter(knowledge_node=node)


    # XXX: use paginator to assure only 25 results will be returned each time
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
        #print(d)
    
    return HttpResponse(json.dumps(d))
    
    
    #return HttpResponse('OK')

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
def ajax_get_page_count_by_section(request):
    section_id = request.GET.get('section_id', '')

    if not section_id:
        return HttpResponse('failed: section_id missing')
    try:
        section = Section.objects.get(pk=section_id)
    except:
        return HttpResponse('failed: section not found with this id')

    questions = Question.objects.filter(knowledge_node__in=json.loads(section.nodes_list))

    return HttpResponse((len(questions.all()) + 24)/25)

@login_required
def ajax_get_questions_by_section(request):
    section_id = request.GET.get('section_id', '')
    page = request.GET.get('page', '1')
    page = int(page)

    if not section_id:
        return HttpResponse('failed: section_id missing')
    try:
        section = Section.objects.get(pk=section_id)
    except:
        return HttpResponse('failed: section not found with this id')

    questions = Question.objects.filter(knowledge_node__in=json.loads(section.nodes_list))
    
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
        subject = request.GET.get('subject', '')
        knowledge_node = request.GET.get('knowledge_node', '')

        f = QuestionQueryForm()

        if subject == '' and knowledge_node == '':
            return render(request, 'quiz/compose_quizs.html', {'form': f})

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

        return render(request, 'quiz/compose_quizs.html', {'questions': questions, 'form': f})

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

