from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from webapps.quiz.models import *
from django.forms import ModelForm
from django.contrib.admin.views.decorators import staff_member_required
from webapps.knowledge_space.models import *

# Create your views here.

@login_required
def start_practice_session(request):
    pass

@login_required
def get_next_question(request):
    pass

@login_required
def question_analysis(request):
    # decision tree
    # 1, locate knowledge node
    # 2, find key variables
    # 3, redo the question
    pass

@login_required
def anwser_question(request):
    if request.method == 'GET':
    
        question_id = request.GET.get('question_id', '')
        if question_id == '':
            return render(request, 'practice/answer_question.html')
        try:
            question = Question.objects.get(id=question_id)
        except:
            return HttpResponse('question not found')
        
        return render(request, 'practice/answer_question.html', {'question': question})

    if request.method == 'POST':
        question_id = request.POST.get('question_id', '')
        print(request.POST)
        option_id = request.POST.get('option_id', '')

        if question_id == '' or option_id == '':
            print(1)
            return render(request, 'practice/answer_question.html', {'error': 'not answered'})

        try:
            question = Question.objects.get(id=question_id)
        except:
            print(2)
            return HttpResponse('question not found')
        try:
            option = Option.objects.get(id=option_id)
        except:
            print(3)
            return HttpResponse('option not found')
    
        # TODO
        #option.update_stat()
        #user.profile.update_stat()
        if option.is_correct and option.question == question:
            print(4)
            return render(request, 'practice/answer_question.html', {'question': question, 'message': 'correct'})
        else:
            print(5)
            return render(request, 'practice/answer_question.html', {'question': question, 'message': 'wrong'})
