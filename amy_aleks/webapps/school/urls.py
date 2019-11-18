from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add-student-to-class', views.add_student_to_class, name='add-student-to-class'),
    url(r'remove-student-from-class', views.remove_student_from_class, name='remove-student-from-class'),
    url(r'add-class', views.add_class, name='add-class'),
    url(r'get-classes', views.get_classes, name='school-get-classes'),
    url(r'^ajax-get-own-classes/$',views.ajax_get_own_classes,name='ajax-get-own-classes'),
    url(r'get-class-detail', views.get_class_detail, name='school-get-class-detail'),
    url(r'pay-student-plan', views.pay_student_plan, name='pay-student-plan'),
    url(r'create-class', views.create_class, name='create-class'),
    url(r'get-all-teachers', views.get_all_teachers, name='get-all-teachers'),
    url(r'get-teachers',views.get_teachers, name='get-teachers'),
    url(r'^ajax-get-school-name',views.ajax_get_school_name,name='ajax-get-school-name'),
    url(r'^school-profile',views.school_profile,name='school-profile'),
    url(r'^ajax-get-cls',views.ajax_get_cls,name='ajax-get-cls'),
    url(r'^delete-class',views.delete_class,name='delete-class'),
    url(r'^ajax-update-school',views.ajax_update_school,name='ajax-update-school'),
]
