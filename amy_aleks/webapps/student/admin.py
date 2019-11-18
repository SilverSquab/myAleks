from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(StudentQuestionRecord)
admin.site.register(StudentQuizRecord)
admin.site.register(StudentKnowledgeAssessment)
admin.site.register(StudentReportPaper)
