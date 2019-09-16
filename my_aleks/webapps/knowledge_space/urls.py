from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'upload-knowledge-nodes/$', views.upload_knowledge_nodes, name='upload-knowledge-nodes'),
    url(r'upload-knowledge-edges/$', views.upload_knowledge_edges, name='upload-knowledge-edges'),
    url(r'ajax-nodes/$', views.ajax_nodes, name='ajax-nodes'),
    url(r'ajax-subjects/$', views.ajax_subjects, name='ajax-subjects'), 
    url(r'ajax-upload-edge/$', views.ajax_upload_edge, name='ajax-upload-edge'),

    url(r'^upload-edge/$', views.upload_edge, name='upload-edge'),
]
