from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'upload-knowledge-nodes/$', views.upload_knowledge_nodes, name='upload-knowledge-nodes'),
    url(r'upload-knowledge-edges/$', views.upload_knowledge_edges, name='upload-knowledge-edges'),
    url(r'ajax-nodes/$', views.ajax_nodes, name='ajax-nodes'),
    url(r'ajax-subjects/$', views.ajax_subjects, name='ajax-subjects'), 
    url(r'ajax-upload-edge/$', views.ajax_upload_edge, name='ajax-upload-edge'),
    url(r'get-node-chineseName',views.get_node_chineseName,name='get-node-chineseName'),

    url(r'^upload-edge/$', views.upload_edge, name='upload-edge'),
    url(r'^ajax-delete-edge-question',views.ajax_delete_edge_question,name='ajax-delete-edge-question'),
    url(r'^get-student-graph-vector/$', views.get_student_graph_vector, name='get-student-graph-vector'),
    url(r'^get-cls-graph-vector/$', views.get_cls_graph_vector, name='get-cls-graph-vector'),
    url(r'^get-student-section-vector/$', views.get_student_section_vector, name='get-student-section-vector'),
    url(r'^get-cls-section-vector/$', views.get_cls_section_vector, name='get-cls-section-vector'),
    url(r'^get-student-chapter-vector/$', views.get_student_chapter_vector, name='get-student-chapter-vector'),
    url(r'^get-cls-chapter-vector/$', views.get_cls_chapter_vector, name='get-cls-chapter-vector'),
]
