from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^question/$', views.question_page, name='question-page'),
    url(r'^get-questions', views.get_questions, name = 'get-questions'),

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
    url(r'^ajax-get-page-count-questions/$', views.ajax_get_page_count_questions, name='ajax-get-page-count-questions'),
    url(r'^ajax-get-own-questions/$', views.ajax_get_own_questions, name='ajax-get-own-questions'),
    url(r'^add-question-to-favorites/$', views.add_question_to_favorites, name='add-question-to-favorites'),

    url(r'^ajax-delete-questions/$',views.ajax_delete_question, name='ajax_delete_question'),
    url(r'^ajax-get-own-question-by-id/$',views.ajax_get_own_question_by_id,name='ajax-get-own-question-by-id'),
    url(r'^ajax-save-quiz-record/$',views.ajax_save_quiz_record,name='ajax-save-quiz-records'),
    url(r'^ajax-save-quiz-and-publish',views.ajax_save_quiz_and_publish,name="ajax-save-quiz-and-publish"),

    url(r'^compose-quizs/$', views.compose_quizs, name='compose-quizs'),
    # get next question when practicing
    url(r'^get-next-question/$', views.get_next_question, name='get-next-question'),

    url(r'^ajax-get-questions-by-section/$', views.ajax_get_questions_by_section, name='ajax-get-questions-by-section'),
    url(r'^ajax-get-page-count-by-section/$', views.ajax_get_page_count_by_section, name='ajax-get-page-count-by-section'),

    url(r'^ajax-get-questions-by-chapter/$', views.ajax_get_questions_by_chapter, name='ajax-get-questions-by-chapter'),
    url(r'^ajax-get-page-count-by-chapter/$', views.ajax_get_page_count_by_chapter, name='ajax-get-page-count-by-chapter'),
    # url(r'^ajax-get-class-report-by-class-id/$', views.ajax_get_class_report_by_class_id, name='ajax-get-class-report-by-class-id'),
    url(r'^get-class-quiz-report/$', views.get_class_quiz_report, name='get-class-quiz-report'),
    url(r'^student-quiz-record/$', views.student_quiz_record, name='student-quiz-record'),

    url(r'^check-questions/$', views.check_questions, name='check-questions'),
    url(r'^my-questions/$', views.my_questions, name='my-questions'),
    url(r'^my-favorites/$', views.my_favorites, name='my-favorites'),
    url(r'^remove-favorites/$', views.remove_favorites, name='remove-favorites'),
    url(r'^add-favorites/$', views.add_favorites, name='add-favorites'),
    url(r'^ajax-get-quiz-questions-information/$', views.ajax_get_quiz_questions_information, name='ajax-get-quiz-questions-information'),
    
    url(r'^upload-completion',views.upload_completion, name='upload-completion'),
    url(r'^ajax-upload-completion-answer', views.ajax_upload_completion_answer, name='ajax-upload-completion-answer')

]
