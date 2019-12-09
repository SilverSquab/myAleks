from django.db import models

# Create your models here.

class ScheduleEvent(models.Model):
    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    title = models.CharField(max_length=100, blank=False, null=False)

    description = models.TextField(max_length=200, blank=False, null=False)
    created_time = models.DateTimeField(null=False, blank=False)

    school = models.ForeignKey('school.School', blank=True, null=True)
    cls = models.ForeignKey('school.Cls', blank=True, null=True)

    YEAR = 'Y'
    MONTH = 'M'
    WEEK = 'W'
    DAY = 'D'
    RULE_CHOICES = (
        (YEAR, 'year'),
        (MONTH, 'month'),
        (WEEK, 'week'),
        (DAY, 'day'),
    )
    rule = models.CharField(max_length=1, choices=RULE_CHOICES)

    end_recurring_period = models.DateTimeField(null=True, blank=True)
    weekday = models.CharField(max_length=10, blank=True, null=True)

class ScheduleOccurrence(models.Model):
    description = models.TextField(max_length=100, blank=True, null=True)

    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    event = models.ForeignKey(ScheduleEvent, blank=False, null=True)

    teacher = models.ForeignKey('teacher.TeacherProfile', blank=True, null=True)
    cls = models.ForeignKey('school.Cls', blank=True, null=True)

    original_start = models.DateTimeField(null=True, blank=True)
    original_end = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=100, blank=False, null=True)
    is_attend_class = models.BooleanField(default=False)
