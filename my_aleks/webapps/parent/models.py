from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ParentProfile(models.Model):
    student = models.ManyToManyField('student.StudentProfile')
    user = models.ForeignKey(User, blank=True, null=True)

    name = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    info = models.TextField(max_length=2000, default='')

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    phone = models.CharField(max_length=12, unique=True, blank=True, null=True, db_index=True)
