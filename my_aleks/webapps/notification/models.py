from django.db import models

# Create your models here.
class Notification(models.Model):
    # sender: <type>_<id>, type chosen from School, TeacherProfile, StudentProfile.. id means its pk in database
    sender = models.CharField(max_length=100, blank=True, null=True)
    receiver = models.CharField(max_length=100, blank=False, null=False)
    msg = models.TextField(max_length=1000, blank=False, null=False)
    msg_type = models.CharField(max_length=50, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    info = models.CharField(max_length=100, blank=True, null=True)
