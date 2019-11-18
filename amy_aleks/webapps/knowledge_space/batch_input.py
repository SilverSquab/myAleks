from .models import *

def generate_dict(s):
    #print(s)
    #print(type(s))
    if s[-1] == '\n':
        s = s[:-1]
    fields = s.split(' ')[0:2]
    #print(fields)
    d = {}
    for field in fields:
        try:
            k, v = field.split(':')
        except:
            #print('wrong format')
            raise Exception('wrong format')
            break
        if v[-1] == '\r':
            v = v[:-1]
        d[k] = v
    
    #print(d)
    return d


def read_knowledge_nodes_from_file(f):
    while True:
        s = str(f.readline(), encoding='utf-8')
        if not s:
            return
        
        d = generate_dict(s)
        
        #print(d)
        #print(d['graph'])
        graph = KnowledgeGraph.objects.get(id=d['graph'])

        node = KnowledgeNode(description=d['description'], graph=graph)
        node.save()

def read_knowledge_edges_from_file(f):
    while True:
        s = str(f.readline(), encoding='utf-8')
        if not s:
            return
        
        d = generate_dict(s)
        
        #print(d)
        p = KnowledgeNode.objects.get(id=d['predecessor'])
        s = KnowledgeNode.objects.get(id=d['successor'])
        if not 'weight' in d.keys():
            d['weight'] = 1

        edge = KnowledgeGraphEdge(predecessor=p, successor=s, weight=d['weight'])

        edge.save()
