from .models import *

def get_predecessors(node_id):
    try:
        node = KnowledgeNode.objects.get(pk=node_id)
    except:
        return {'status': False, 'reason': 'node does not exist'}

    
    edges = KnowledgeGraphEdge.objects.filter(successor=node)
    return {'status': True, 'nodes': edges.values_list('predecessor__pk', flat=True)}

def get_successors(node_id):
    try:
        node = KnowledgeNode.objects.get(pk=node_id)
    except:
        return {'status': False, 'reason': 'node does not exist'}

    edges = KnowledgeGraphEdge.objects.filter(predecessor=node)
    return {'status': True, 'nodes': edges.values_list('successor__pk', flat=True)}
