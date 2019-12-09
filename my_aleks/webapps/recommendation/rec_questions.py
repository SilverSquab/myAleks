def recommend_questions_by_graph(student_no, graph_id):
    return []

def recommend_questions_by_graphs(student_no, graph_list):
    question_list = []
    for graph_id in graph_list:
        question_list.append(recommend_questions_by_graph(student_no, graph_id))

    return question_list

def recommend_question_by_node(student_no, node_id, question_count=1):
    try:
        node = KnowledgeNode.objects.get(pk=node_id)
    except:
        return {'status': False, 'reason': 'node not existed'}

    questions = node.question_set.all()
    # TODO: get random questions from questions
    return []
