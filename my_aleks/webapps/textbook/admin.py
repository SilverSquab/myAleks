from django.contrib import admin
from .models import *

class PartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'section', 'id', 'get_chapter')

class TextbookAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'publisher')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'chapter', 'id')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'textbook')

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Textbook, TextbookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Part, PartAdmin)
