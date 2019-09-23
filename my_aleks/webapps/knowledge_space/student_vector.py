from webapps.student.models import StudentProfile
from .models import *
import json

# get a specific vector for a graph
def get_or_create_graph_vector(student_id, graph_id):
    profile = StudentProfile.objects.get(student_id)
    try:
        vectors = json.loads(profile.vectors)
    except:
        raise ValueError('vector not formalized')
    
    try:
        graph = KnowledgeGraph.objects.get(pk=graph_id)
    except:
        raise Exception('graph not existed')

    if graph_id in vectors:
        return vectors[graph_id]

    else:
        vectors[graph_id] = {}

