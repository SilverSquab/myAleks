"""my_aleks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin 
from webapps.user.views import login_view,logout_view
from django.conf.urls.static import static
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/abc/media/'

urlpatterns = [
    url(r'^abc/admin/', admin.site.urls),
    #url(r'^abc/xadmin/', xadmin.site.urls),
    url(r'^abc/teacher/',include('webapps.teacher.urls'),name="teacher-url"),
    url(r'^abc/student/',include('webapps.student.urls'),name="student-url"),
    url(r'^abc/quiz/',include('webapps.quiz.urls'),name="quiz-url"),
    url(r'^abc/login/',login_view,name="login"),
    url(r'^abc/logout/',logout_view,name="logout"),
    url(r'^abc/practice/',include('webapps.practice.urls'), name="practice-url"),
    url(r'^abc/ks/',include('webapps.knowledge_space.urls'), name="knowledge-space-url"),
    url(r'^abc/school/',include('webapps.school.urls'), name="school-url"),
    url(r'^abc/plan/',include('webapps.plan.urls'), name="plan-url"),
    url(r'^abc/user/',include('webapps.user.urls'), name="user-url"),
    url(r'^abc/textbook/',include('webapps.textbook.urls'), name="textbook-url"),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
