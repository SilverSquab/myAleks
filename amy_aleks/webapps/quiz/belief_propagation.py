import pymongo
mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)

def weighted_average(dic):
    sum_ = 0
    weight_sum = 0
    for key in dic:
        sum_ += key * dic[key]
        weight_sum += dic[key]
    if weight_sum == 0:
        raise ValueError('weight added up to 0')
    return float(sum_) / weight_sum
    
# is_question: whether this update comes from a question
# is_correct: if this is correct
def update_node(student_id, node_id, belief, score, is_question=True, is_correct=False):
    collection = mongoclient.student_log.question_records
    try:
        doc = collection.find_one({'student_id': student_id, 'node_id': node_id})
    except:
        return False

    if not doc:
        doc = {
            'student_id': student_id,
            'node_id': node_id,
            'belief': belief,
            'score': score,
            'num_questions': (1 if is_question else 0),
            'num_correct': (1 if is_question and is_correct else 0),
            'correct_rate': (1 if is_question and is_correct else 0),
        }
        collection.insert_one(doc)
        return True
    
    dic = {doc['score']: doc['belief'], score: belief}
    new_score = weight_average(dic)
    new_belief = belief + doc['belief']
    if new_belief >= 2.0:
        new_belief = 2.0
    num_questions = doc['num_questions']
    num_correct = doc['num_correct']
    if is_question:
        num_questions = doc['num_questions'] + 1
        if is_correct:
            num_correct = doc['num_correct'] + 1
    correct_rate = float(num_correct) / num_questions
    try:        
        collection.update_one(
            {'student_id': student_id, 'node_id': node_id},
            {
                '$set': {
                    'belief': new_belief,
                    'score': new_score,
                    'num_questions': num_questions,
                    'num_correct': num_correct,
                    'correct_rate': correct_rate;
                }
            }
        )
    except Exception as e:
        print(e)
        return False
    return True
