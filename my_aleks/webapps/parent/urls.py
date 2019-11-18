from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^update-parent/$', views.update_parent, name='update-parent'),
]
