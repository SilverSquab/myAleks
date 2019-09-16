from django.core import serializers
from .models import *

f = open('knowledge_space_serialized.txt', 'w+')


subjects = serializers.serialize("xml", Subject.objects.all())
f.write(subjects)
knowledgeGraphs = serializers.serialize("xml", KnowledgeGraph.objects.all())
f.write(knowledgeGraphs)
knowledgeNodes = serializers.serialize("xml", KnowledgeNode.objects.all())
f.write(knowledgeNodes)
knowledgeGraphEdges = serializers.serialize("xml", KnowledgeGraphEdge.objects.all())
f.write(knowledgeGraphEdges)
errorReasons = serializers.serialize("xml", ErrorReason.objects.all())
f.write(errorReasons)
