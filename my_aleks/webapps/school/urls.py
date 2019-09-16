from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add-student-to-class', views.add_student_to_class, name='add-student-to-class'),
    url(r'remove-student-from-class', views.remove_student_from_class, name='remove-student-from-class'),
    url(r'add-class', views.add_class, name='add-class'),
    url(r'get-classes', views.get_classes, name='school-get-classes'),
    url(r'get-class-detail', views.get_class_detail, name='school-get-class-detail'),
    url(r'pay-student-plan', views.pay_student_plan, name='pay-student-plan'),
    url(r'create-class', views.create_class, name='create-class'),
    url(r'get-all-teachers', views.get_all_teachers, name='get-all-teachers'),
]
