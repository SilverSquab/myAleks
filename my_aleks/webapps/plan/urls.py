from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'ajax-get-plan-templates', views.ajax_get_plan_templates, name='ajax-get-plan-templates'),
    url(r'assign-plan-to-class', views.assign_plan_to_class, name='assign-plan-to-class'),
]
