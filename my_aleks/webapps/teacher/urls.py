from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='teacher-index'),
    url(r'^view-student/', views.view_student, name='view-student'),
    url(r'^view-class/', views.view_class, name='view-class'),
    url(r'^my-classes/', views.my_classes, name='my-classes'),
    url(r'^my-quizes/', views.my_quizes, name='my-quizes'),
]
