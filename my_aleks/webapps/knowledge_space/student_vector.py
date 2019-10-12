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
    
    #get student profile by id
    try:
        profile = StudentProfile.objects.get(pk=student_id)
    except:
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
            d[node] = {"belief" : 1, "score": 0.5}

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
            d[node] = {"belief" : 1, "score": 0.5}

        vectors[graph_id] = d
        
        col.update({'student_id': student_id}, {'student_id': student_id, 'vectors': vectors})
        
    result['status'] = 'success'
    result['data'] = vectors[graph_id]
    return json.dumps(result)

    
def get_cls_graph(cls_id, graph_id):
    result = {}
    try:
        cls = Cls.objects.get(pk=cls_id)
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
    students = StudentProfile.objects.filter(pk__in=json.loads(cls.students))
    #print(students)
    #print(students.values_list('pk', flat=True))
    dicts = list(map(foo, students.values_list('pk', flat=True)))
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

    ret = {}
    ret['status'] = 'success'
    ret['data'] = result

    return json.dumps(ret)
        
    

