from django.db import models

# Create your models here.

# for us administrator
class PlanTemplate(models.Model):
    description = models.TextField(max_length=200, blank=True, null=True)
    name = models.TextField(max_length=100, blank=True, null=True)
    resources = models.TextField(max_length=500, default='{}')
    default_price = models.IntegerField(default=1)
    subject = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    info = models.CharField(max_length=500, default='{}')

# for a class
class Plan(models.Model):
    cls = models.ForeignKey('school.Cls', blank=False, null=False)
    price = models.IntegerField(default=1)
    template = models.ForeignKey(PlanTemplate, blank=True, null=True)
    resources = models.TextField(max_length=500, default='{}')
    remaining_resources = models.TextField(max_length=500, default='{}')
    description = models.TextField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    info = models.CharField(max_length=500, default='{}')

class StudentPlan(models.Model):
    student = models.ForeignKey('student.StudentProfile', blank=False, null=False)
    price = models.IntegerField(default=1)
    plan = models.ForeignKey(Plan, blank=True, null=True)
    payment_record = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    #one of cls and plan must not be null
    cls = models.ForeignKey('school.Cls', blank=True, null=True)

    resources = models.TextField(max_length=500, default='{}')
    remaining_resources = models.TextField(max_length=500, default='{}')
    description = models.TextField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    info = models.CharField(max_length=500, default='{}')
