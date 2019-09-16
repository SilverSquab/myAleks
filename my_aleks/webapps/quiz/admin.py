from django.contrib import admin
from .models import *

# Register your models here.

class OptionAdmin(admin.ModelAdmin):
    exclude = ('question',)

admin.site.register(Question)
admin.site.register(Option, OptionAdmin)
admin.site.register(QuestionStat)
admin.site.register(OptionStat)
admin.site.register(Quiz)
admin.site.register(QuizRecord)
admin.site.register(QuizStat)
