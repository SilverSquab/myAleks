from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.

# version of books
class Publisher(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=False, null=False)
    chinese_name = models.CharField(max_length=40, blank=True, null=True)
    version_name = models.CharField(max_length=40, blank=True, null=True)
    def __str__(self):
        return (self.name + ' ' + self.chinese_name) or u'None'

class Textbook(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=40, blank=False, null=False)
    chinese_name = models.CharField(max_length=40, blank=True, null=True)
    grade = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    # range from 1 to 12
    grade_no = models.CharField(max_length=5, db_index=True, blank=True, null=True)
    # first or second half, represented as 1 or 2
    half = models.CharField(max_length=5, blank=True, null=True)
    
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    def __str__(self):
        return (self.grade + ' '  + self.chinese_name) or u'None'

class Chapter(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    chinese_name = models.CharField(max_length=40, blank=True, null=True)

    # no. of chapters, can either be numbers or chinese letters
    order = models.CharField(max_length=20, blank=True, null=True)
    
    textbook = models.ForeignKey(Textbook, blank=True, null=True, related_name='chapters')
    def __str__(self):
        return self.order + ' ' + self.chinese_name or u'None'

class Section(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    chinese_name = models.CharField(max_length=40, blank=True, null=True)

    order = models.CharField(max_length=20, blank=True, null=True)

    chapter = models.ForeignKey(Chapter, blank=True, null=True, related_name='sections')

    # only recording nodes that don't fit in any parts of this section
    nodes_list = models.TextField(max_length=500, default='[]')
    def __str__(self):
        return self.order + ' ' + self.chinese_name or u'None'

class Part(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    chinese_name = models.CharField(max_length=40, blank=True, null=True)

    order = models.CharField(max_length=20, blank=True, null=True)

    section = models.ForeignKey(Section, blank=True, null=True, related_name='parts')

    nodes_list = models.TextField(max_length=500, default='[]')
    def __str__(self):
        return self.section.chapter.textbook.publisher.chinese_name + ' ' + self.section.chapter.textbook.chinese_name + ' ' + self.order + ' ' + self.chinese_name
        #return (self.section.chapter.textbook.publisher.chinese_name + ' ' + self.section.chapter.textbook.chinese_name + ' ' + self.section.chapter.chinese_name + ' ' + self.section.chinese_name + ' '+  self.chinese_name) or u'None'

    def get_chapter(self):
        return str(self.section.chapter)
