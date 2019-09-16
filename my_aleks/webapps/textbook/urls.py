from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'upload-textbooks', views.ajax_upload_textbooks, name='upload-textbooks'),
    url(r'ajax-get-all-textbooks', views.ajax_get_all_textbooks, name='ajax-get-all-textbooks'),
    url(r'ajax-get-textbook-structure', views.ajax_get_textbook_structure, name='ajax-get-textbook-structure'),
]
