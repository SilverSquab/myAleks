from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TeacherProfile(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    phone = models.CharField(max_length=12, blank=False, null=False, db_index=True)
    subject = models.ForeignKey('knowledge_space.Subject', blank=False, null=False)
    school = models.ForeignKey('school.School', blank=True, null=True)
    # including grade
    info = models.TextField(max_length=2000, blank=True, null=True, default='')
    # all kinds of stats
    stats = models.TextField(max_length=2000, blank=True, null=True, default='')

    user = models.OneToOneField(User, blank=False, null=False)
    
    img = models.ImageField(blank=True, null=True, upload_to='teacher_imgs')

class Favorites(models.Model):
    teacher = models.OneToOneField(TeacherProfile, blank=False, null=False)
    questions = models.ManyToManyField('quiz.Question', blank=True, null=True)
