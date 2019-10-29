'''
algorithm module.
only update node after a question is answered
'''
from webapps.student.models import StudentProfile
from webapps.school.models import Cls
from .student_vector import get_or_create_graph_vector
from .models import *
import json
import pymongo
import json

mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)

def update_nodes(student_id, nodes_dic, belief = 3):
    student_id = str(student_id)
    vectors = {}
    col = mongo_client.student_log.student_ks_vector

    # find or create student vector object
    vector_obj = col.find_one({"student_id": student_id})
    if vector_obj == None:
        col.insert_one({"student_id": student_id, "vectors": {}})
        vector_obj = col.find_one({"student_id": student_id})

    # round robin all graphs
    vectors = vector_obj['vectors']
    for node_id in nodes_dic:
        try:
            node = KnowledgeNode.objects.get(pk=node_id)
        except:
            return {'status': False, 'reason': 'node not exited'}

        graph_id = node.graph.pk
        if graph_id not in vectors:
            vectors[graph_id] = json.loads(get_or_create_graph_vector(student_id, graph_id))['data']
            
            #vector_obj = 
        
        if not node_id in vectors[graph_id]:
            vectors[graph_id][node_id] = {'belief':1, 'score': 0.6}
        old_belief = vectors[graph_id][node_id]['belief']
        score = vectors[graph_id][node_id]['score']
        score = (score * old_belief + nodes_dic[node_id] * belief) / (old_belief + belief)
        new_belief = old_belief + belief

        if new_belief >= 3:
            new_belief = 3
        

        vectors[graph_id][node_id] = {'score': score, 'belief': new_belief}


    col.update({'student_id': student_id}, {'student_id': student_id, 'vectors': vectors})
        
