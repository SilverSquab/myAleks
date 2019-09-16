from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PracticeSession(models.Model):
    student = models.ForeignKey(User, blank=False, null=False)
    subject = models.CharField(max_length=20, blank=False, null=False)
    knowledge_space = models.CharField(max_length=100, blank=True, null=True)
    knowledge_space_nodes = models.TextField(max_length=200, blank=True, null=True)
    route = models.TextField(max_length=1000, default='')
