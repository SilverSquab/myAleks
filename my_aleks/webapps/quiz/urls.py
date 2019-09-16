from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^question/$', views.question_page, name='question-page'),

    url(r'^questions/$', views.questions_page, name='questions-page'),
    url(r'^compose-quiz/$', views.compose_quiz, name='compose-quiz'),
    url(r'^quiz/$', views.quiz_page, name='quiz-page'),
    url(r'^mark-quiz/$', views.mark_quiz, name='mark-quiz'),
    url(r'^mark-question/$', views.mark_question, name='mark-question'),
    url(r'^quiz-records/$', views.quiz_records, name='quiz-records'),
    url(r'^quiz-record/$', views.quiz_record, name='quiz-record'),
    url(r'^upload-question/$', views.upload_question, name='upload-question'),

    url(r'^ajax-upload-question/$', views.ajax_upload_question, name='ajax-upload-question'),
    url(r'^ajax-upload-option/$', views.ajax_upload_option, name='ajax-upload-option'),
    url(r'^ajax-get-questions/$', views.ajax_get_questions, name='ajax-get-questions'),
    url(r'^ajax-get-own-questions/$', views.ajax_get_own_questions, name='ajax-get-own-questions'),
    url(r'^add-question-to-favorites/$', views.add_question_to_favorites, name='add-question-to-favorites'),

    url(r'^compose-quizs/$', views.compose_quizs, name='compose-quizs'),

    url(r'^ajax-get-questions-by-section/$', views.ajax_get_questions_by_section, name='ajax-get-questions-by-section'),
    url(r'^ajax-get-page-count-by-section/$', views.ajax_get_page_count_by_section, name='ajax-get-page-count-by-section'),
]
