from __future__ import unicode_literals

from django.db import models
from uuid import uuid4

def get_uuid4():
    return str(uuid4())[-12:]

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=20, primary_key=True, blank=False, null=False)
    chinese_name = models.CharField(max_length=40, blank=True, null=True)
    icon = models.ImageField(blank=True, null=True, upload_to='subject_icons')
    def __str__(self):
        return self.name

#class Chapter(models.Model):
#    name = models.CharField(max_length=50, primary_key=True, blank=False, null=False, db_index=True)
#    textbook = models.CharField(max_length=50, blank=True, null=True)
#    def __str__(self):
#        return self.name
    

class KnowledgeGraph(models.Model):
    id = models.CharField(primary_key=True, default=get_uuid4, max_length=20)
    uri = models.CharField(max_length=100, default='None')
    subject = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    description = models.TextField(max_length=20, blank=False, null=False)
    def __str__(self):
        return self.description

class KnowledgeNode(models.Model):
    id = models.CharField(primary_key=True, default=get_uuid4, max_length=20)
    description = models.TextField(max_length=200, blank=False, null=False)
    graph = models.ForeignKey(KnowledgeGraph, blank=False, null=False)
    title = models.TextField(max_length=200, blank=True, null=True)

    #chapter = models.ForeignKey(Chapter, blank=True, null=True)
    def __str__(self):
        return self.description

class KnowledgeGraphEdge(models.Model):
    id = models.CharField(primary_key=True, default=get_uuid4, max_length=20)
    predecessor = models.ForeignKey(KnowledgeNode, related_name='successors', blank=False, null=False)
    successor = models.ForeignKey(KnowledgeNode, related_name='predecessors', blank=False, null=False)
    weight = models.FloatField(default=1.0)
    def __str__(self):
        return str(self.predecessor) + ' ' + str(self.successor)

class ErrorReason(models.Model):
    id = models.CharField(primary_key=True, default=get_uuid4, max_length=20)
    description = models.TextField(max_length=200, blank=False, null=False)
    knowledge_node = models.ForeignKey(KnowledgeNode, blank=False, null=False)
    #other info, such as logic weakness or something
    info = models.TextField(max_length=1000, blank=True, null=True)
    weight = models.FloatField(default=1.0)
    def __str__(self):
        return self.description

