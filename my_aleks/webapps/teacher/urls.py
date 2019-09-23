from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='teacher-index'),
    url(r'^view-student/', views.view_student, name='view-student'),
    url(r'^view-class/', views.view_class, name='view-class'),
    url(r'^my-classes/', views.my_classes, name='my-classes'),
    url(r'^my-quizes/', views.my_quizes, name='my-quizes'),

    url(r'^ajax-get-class-report-by-class-id',views.ajax_get_class_report_by_class_id, name='ajax-get-class-report-by-class-id'),
    url(r'^ajax-get-scores-student',views.ajax_get_scores_student, name='ajax-get-scores-student'),
    url(r'^ajax-get-scores-class',views.ajax_get_scores_class,name='ajax-get-scores-class'),
]
