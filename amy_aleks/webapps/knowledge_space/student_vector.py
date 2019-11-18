from webapps.student.models import StudentProfile
from webapps.school.models import Cls
from .models import *
import json
import pymongo
import json

mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)

# get a specific vector for a graph
def get_or_create_graph_vector(student_id, graph_id):
    student_id = str(student_id)
    graph_id = str(graph_id)
    result = {}
    #print(student_id)
    #get student profile by id
    try:
        profile = StudentProfile.objects.get(student_no=student_id)
        #print(profile)
    except:
       # print(1)
        result['status'] = 'fail'
        result['reason'] = 'student not existed'
        return json.dumps(result)
        
    #get graph
    try:
        graph = KnowledgeGraph.objects.get(pk=graph_id)
    except:
        result['status'] = 'fail'
        result['reason'] = 'graph not existed'
        return json.dumps(result)

    col = mongo_client.student_log.student_ks_vector
    #create new graph vector
    vector_obj = col.find_one({"student_id": student_id})
    if vector_obj == None:
        d = {}
        nodes = graph.knowledgenode_set.values_list('id', flat=True)
        for node in nodes:
            d[node] = {"belief" : 1, "score": 0.6}

        col.insert_one({"student_id": student_id, "vectors":{graph_id:d}})
        vector_obj = col.find_one({"student_id": student_id})

    #graph_id already in vectors
    vectors = vector_obj['vectors']
    if graph_id in vectors:
        result['status'] = 'success'
        result['data'] = vectors[graph_id]
        return json.dumps(result)

    #graph not in vectors
    else:
        d = {}
        nodes = graph.knowledgenode_set.values_list('id', flat=True)
        for node in nodes:
            d[node] = {"belief" : 1, "score": 0.6}

        vectors[graph_id] = d
        
        col.update({'student_id': student_id}, {'student_id': student_id, 'vectors': vectors})
        
    result['status'] = 'success'
    result['data'] = vectors[graph_id]
    return json.dumps(result)

    
def get_cls_graph(cls_id, graph_id):
    result = {}
    try:
        cls = Cls.objects.get(pk=cls_id,deleted=False)
    except:
        result['status'] = 'fail'
        result['reason'] = 'cls not existed'
        return json.dumps(result)
    
    def foo(student_id):
        #print(get_or_create_graph_vector(student_id, graph_id))
        d = json.loads(get_or_create_graph_vector(student_id, graph_id))
        if d['status'] == 'success':
            return d['data']
        else:
            return {}

    #print(cls.students)
    students = StudentProfile.objects.filter(student_no__in=json.loads(cls.students))
    #print(students.values_list('pk', flat=True))
    dicts = list(map(foo, students.values_list('student_no', flat=True)))
    #print(dicts)
    if len(dicts) == 0:
        result['status'] = 'fail'
        result['reason'] = 'no student vector available'
        return json.dumps(result)
    result = {}
    keys = list(dicts[0].keys())
    def dict_average(dict_list, key):
        s = 0
        cnt = 0
        for d in dict_list:
            if key in d:
                s = float(s)
                s += float(d[key]['score'])

                cnt += 1
        if cnt == 0:
            return 0
        return float(s)/float(cnt)

    for key in keys:
        result[key] = dict_average(dicts, key)
    #print(result)
    ret = {}
    ret['status'] = 'success'
    ret['data'] = result

    return json.dumps(ret)
        
    
def get_node_scores(student_id, nodes_list):
    nodes = KnowledgeNode.objects.filter(pk__in=nodes_list)
    #get graphs
    graphs = list(set(nodes.values_list('graph', flat=True)))
    dic = {}
    for graph_pk in graphs:
        graph_vector = json.loads(get_or_create_graph_vector(student_id, graph_pk))
        if graph_vector['status'] == 'success':
            dic.update(graph_vector['data'])
    
    #filter scores we need from whole graph vectors
    scores = {}
    for node_pk in nodes_list:
        if node_pk in dic:
            scores[node_pk] = dic[node_pk]
    return scores

def get_node_score(student_id, node_id):
    try:
        node = KnowledgeNode.objects.get(pk=node_id)
    except:
        return {'status': False, 'reason': 'node does not exist'}

    graph = node.graph
    graph_vector = json.loads(get_or_create_graph_vector(student_id, graph.pk))
    if graph_vector['status'] == 'fail':
        return {'status': False, 'reason': 'cannot get graph vector'}

    return {'status': True, 'score': graph_vector['data'][node_id]}
        
