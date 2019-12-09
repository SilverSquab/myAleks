from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# for now, we asume all questions were multi-choice questions
# will add different logics later
class QuestionRecord(models.Model):
    user = models.ForeignKey('student.StudentProfile', blank=False, null=False, related_name='question_records')
    option = models.ForeignKey('Option', blank=False, null=False, related_name='question_records')
    question = models.ForeignKey('Question', blank=False, null=False, related_name='question_records')
    datetime = models.DateTimeField(auto_now_add=True)
    
    def is_correct(self):
        return self.option.is_correct

class Question(models.Model):
    #id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=40)
    body = models.TextField(max_length=3000, blank=False, null=False)
    subject = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    question_type = models.CharField(max_length=20, default='single-choice')

    knowledge_node = models.ManyToManyField('knowledge_space.KnowledgeNode', blank=False)
    img = models.ImageField(blank=True, null=True, upload_to='question_imgs')
    analysis_img = models.ImageField(blank=True, null=True, upload_to='analysis_imgs')
    
    datetime = models.DateTimeField(auto_now_add = True, blank=True, null=True)

    uploader = models.ForeignKey(User, blank=True, null=True, related_name='questions_uploaded')

    analysis = models.TextField(max_length=2000, blank=True, null=True)

    selected = models.BooleanField(default=False)

    # choose from U: unauthenticated, P: passed, R: rejected
    authenticated = models.CharField(max_length=5, default='U', db_index=True)

    def student_answer_question(self, user, option):
        QuestionRecord.objects.get_or_create(user = user, option = option, question = self)
        self.stat.update_question_stat(option)
        return True

    def __str__(self):
        return self.body
    

class Option(models.Model):
    #id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=40)
    body = models.TextField(max_length=1000, blank=False, null=False)
    # ABCD, 1234 or something
    order = models.CharField(max_length=5, blank=True, null=True)
    question = models.ForeignKey(Question, blank=False, null=False, related_name='options')

    is_correct = models.BooleanField(default=False)

    error_reason = models.ManyToManyField('knowledge_space.ErrorReason', blank=True)
    knowledge_node = models.ManyToManyField('knowledge_space.KnowledgeNode', blank=False)
    img = models.ImageField(blank=True, null=True, upload_to='option_imgs')
    def __str__(self):
        return str(self.order) + ' ' + str(self.body)

class QuestionStat(models.Model):
    correct_rate = models.FloatField(default=0)
    times_answered = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    question = models.OneToOneField(Question, related_name='stat', blank=True, null=True)
    # other high level stats, stored in one textfield for now. need to find a better approach
    info = models.TextField(max_length=1000, blank=True, null=True)

    def update_question_stat(self, option):
        option.option_stat.select_option()
        self.times_answered += 1
        if option.is_correct:
            self.times_correct += 1
        
        self.correct_rate = float(self.times_correct) / self.times_answered
        self.save()

    
class OptionStat(models.Model):
    times_checked = models.IntegerField(default=0)
    #check_rate = models.FloatField(default=0)
    # other high level stats, stored in one textfield for now. need to find a better approach
    info = models.TextField(max_length=1000, blank=True, null=True)
    option = models.OneToOneField(Option, related_name='stat', blank=True, null=True)

    def select_option(self):
        self.times_checked += 1
        self.save()

class Quiz(models.Model):
    #id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=40)
    generator = models.ForeignKey(User, blank=True, null=True)
    subject = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    # other info, such as datetime, school and so forth, XXX: type
    info = models.TextField(max_length=500, default='{}')
    # JSON field like {question: score}
    body = models.TextField(max_length=2000, blank=False, null=False)
    quiz_type = models.CharField(max_length=20, blank=False, null=False, default='suitang')

    public = models.BooleanField(default=False)
    # whether this quiz is to be marked, does every question has a score?
    marking = models.BooleanField(default=False)
    
    # overall stat of this quiz. no regard to quiz record
    stat = models.OneToOneField('QuizStat', blank=True, null=True)

    def __str__(self):
        return self.subject + ' ' + str(self.id)

# quiz record is a quiz taken by a certain class
class QuizRecord(models.Model):
    quiz = models.ForeignKey(Quiz)
    teacher = models.ForeignKey('teacher.TeacherProfile', blank=False, null=False)
    # which class is taking this quiz? that means one quiz can be taken by several classes
    cls = models.ForeignKey('school.Cls', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    info = models.TextField(max_length=1000, blank=True, null=True)

    stats = models.TextField(max_length=2000, default='{}')

    def __str__(self):
        return str(self.id)

class QuizStat(models.Model):
    #quiz = models.ForeignKey(Quiz, blank=False, null=False)

    quiz_record = models.ForeignKey(QuizRecord, blank=False, null=False)

    # ppl who took this quiz
    times_taken = models.IntegerField(default=0)

    average_score = models.FloatField(default=0)

    #scores may not be able to be stored in data base. use a text file
    # stored in file like[[student, score]]
    scores_uri = models.TextField(max_length=100, blank=True, null=True)

    # TODO: need to add a lot of fields later
    stats = models.TextField(max_length=2000, default='')

class QuizPaper(models.Model):
    pdf_uri = models.CharField(max_length=150, blank=False, null=False)
    html_uri = models.CharField(max_length=150, blank=False, null=False)
    quiz = models.ForeignKey(Quiz, blank=True, null=True)

class QuizRecordPaper(models.Model):
    pdf_uri = models.CharField(max_length=150, blank=False, null=False)
    html_uri = models.CharField(max_length=150, blank=False, null=False)
    quiz_record = models.ForeignKey(QuizRecord, blank=True, null=True)

class CompletionAnswer(models.Model):
    body = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, blank=False, null=False, related_name='CompletionAnswer')
    error_reason = models.ManyToManyField('knowledge_space.ErrorReason', blank=True)
    def __str__(self):
        return str(self.body)
