from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class StudentProfile(models.Model):
    teachers = models.ManyToManyField('teacher.TeacherProfile', blank=True)
    clss = models.ManyToManyField('school.Cls', blank=True)
    cls_list = models.CharField(max_length=200, blank=True, null=True, default='[]')
    
    name = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    phone = models.CharField(max_length=12, unique=True, blank=True, null=True, db_index=True)
    image = models.ImageField(max_length=255, blank=True, null=True, upload_to='student_imgs')

    student_no = models.CharField(max_length=20, blank=True, null=True, db_index=True)

    grade = models.IntegerField(default=9)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)

    age = models.IntegerField(default=15)
    #school = models.ForeignKey('school.School', blank=False, null=False)
    # including grade
    info = models.TextField(max_length=2000, default='')
    
    user = models.OneToOneField(User, blank=False, null=False)
    
    def __str__(self):
        return self.name

class StudentQuestionRecord(models.Model):
    student = models.ForeignKey(StudentProfile, blank=True, null=True, db_index=True)
    question = models.ForeignKey('quiz.Question')
    option = models.ForeignKey('quiz.Option')
    # a reserved field for text answer in future
    answer = models.TextField(max_length=200, blank=True, null=True)

    datetime = models.DateTimeField(blank=True, null=True)

    # other info such as how he used prompt
    info = models.TextField(max_length=200, blank=True, null=True)

    # when the question belongs to a quiz
    student_quiz_record = models.ForeignKey('StudentQuizRecord', blank=True, null=True)

    def is_correct(self):
        return self.option.is_correct

class StudentQuizRecord(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(StudentProfile, blank=True, null=True)
    quiz_record = models.ForeignKey('quiz.QuizRecord', blank=False, null=False)
    score = models.FloatField(default=0)
    
    stats = models.TextField(max_length=1000, blank=True, null=True)

class StudentKnowledgeAssessment(models.Model):
    '''
    save these fields as static files. Too big in memory or database
    '''
    knowledge_space_graph_uri = models.TextField(max_length=100, blank=True, null=True)
    learning_router_uri = models.TextField(max_length=100, blank=True, null=True)
    assessment_report_uri = models.TextField(max_length=100, blank=True, null=True)

class StudentKnowledgeVectors(models.Model):
    '''
    vector should be saved in static files. 
    if graph_id is null, this Vector represents the whole picture
    '''
    #graph_id = models.CharField(max_length=50, blank=True, null=True)
    #vector_uri = models.TextField(max_length=100, blank=True, null=True)
    vectors = models.TextField(max_length=20000, blank=True, null=True)
    student = models.ForeignKey(StudentProfile, blank=True, null=True, related_name='vectors')


class StudentReportPaper(models.Model):
    pdf_uri = models.CharField(max_length=150, blank=False, null=False)
    html_uri = models.CharField(max_length=150, blank=False, null=False)
    quiz = models.ForeignKey('quiz.Quiz', blank=True, null=True)
    student = models.ForeignKey(StudentProfile, blank=True, null=True)
    subject = models.CharField(max_length=20, blank=True, null=True)
    datetime = models.DateField(blank=True, null=True)
    new = models.BooleanField(default=True)
    

class Tuition(models.Model):
    remaining_no = models.IntegerField(default=0)
    student = models.ForeignKey(StudentProfile, blank=False, null=False)
    cls = models.ForeignKey('school.Cls', blank=False, null=False)
    school = models.ForeignKey('school.School', blank=True, null=True)
    fee = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
