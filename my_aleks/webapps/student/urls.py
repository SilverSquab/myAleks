from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^index/$', views.student_index, name="student-index"),
    url(r'^student-login/$', views.student_login, name="student-login"),
    url(r'^get-assessment/$', views.get_assessment, name="get-assessment"),
    url(r'^student-quiz-report/$', views.student_quiz_report, name="student-quiz-report"),

    url(r'^student-register', views.student_register, name="student-register"),

    url(r'^ajax-get-student-profile', views.ajax_get_student_profile, name="ajax-get-student-profile"),
    url(r'^student-profile-tuition', views.student_profile_tuition, name="student-profile-tuition"),
    url(r'^ajax-get-class-student', views.ajax_get_class_student, name = "ajax-get-class-student"),
    url(r'^reduce-class', views.reduce_class, name = "reduce-class"),
]
