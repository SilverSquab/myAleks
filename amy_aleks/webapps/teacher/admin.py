from django.contrib import admin
from .models import *

# Register your models here.

class FavoritesAdmin(admin.ModelAdmin):
    exclude = ('questions',)

admin.site.register(TeacherProfile)
admin.site.register(Favorites, FavoritesAdmin)
