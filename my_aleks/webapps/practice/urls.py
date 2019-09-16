from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^answer-question/$', views.anwser_question, name='answer-question'),
]
