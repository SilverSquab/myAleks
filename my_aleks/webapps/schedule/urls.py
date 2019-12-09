from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^ajax-add-schedule-event/', views.ajax_add_schedule_event, name='ajax-add-schedule-event'),
    url(r'^ajax-get-schedule-event-by-class', views.ajax_get_schedule_event_by_class, name = 'ajax-get-schedule-event-by-class'),
    url(r'^ajax-get-schedule-by-school', views.ajax_get_schedule_by_school, name = 'ajax-get-schedule-by-school'),
    url(r'^ajax-delete-schedule-by-id', views.ajax_delete_schedule_by_id, name = 'ajax-delete-schedule-by-id'),    
    url(r'^ajax-update-schedule-event', views.ajax_update_schedule_event, name = 'ajax-update-schedule-event'),
    url(r'^ajax-get-schedule-occurrence-by-class', views.ajax_get_schedule_occurrence_by_class, name = 'ajax-get-schedule-occurrence-by-class'),
    url(r'^ajax-add-schedule-occurrence', views.ajax_add_schedule_occurrence, name = 'ajax-add-schedule-occurrence'),
    url(r'^ajax-update-schedule-occurrence', views.ajax_update_schedule_occurrence, name = 'ajax-update-schedule-occurrence'),
    url(r'^ajax-delete-schedule-occurrence', views.ajax_delete_schedule_occurrence, name = 'ajax-delete-schedule-occurrence'),

]
