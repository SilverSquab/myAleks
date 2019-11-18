from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Subject)
admin.site.register(KnowledgeGraph)
admin.site.register(KnowledgeNode)
admin.site.register(KnowledgeGraphEdge)
admin.site.register(ErrorReason)
#admin.site.register(Chapter)
