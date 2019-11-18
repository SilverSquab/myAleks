from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class School(models.Model):
    name = models.TextField(max_length=50, blank=False, null=False, db_index=True)
    location = models.TextField(max_length=100, blank=True, null=True)
    account = models.IntegerField(default=0)
    manager = models.OneToOneField(User, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)

class Cls(models.Model):
    subject = models.CharField(max_length=20, blank=True, null=True)
    school = models.ForeignKey(School, related_name='classes')
    grade = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    students = models.TextField(max_length=20000, null=True, default='[]')
    num = models.IntegerField(default=0)
    teacher = models.ForeignKey('teacher.TeacherProfile', blank=True, null=True, related_name='classes')
    deleted = models.BooleanField(default=False)
    #TODO: <student, class>tuple

'''
class SchoolCls():
    pass
'''
