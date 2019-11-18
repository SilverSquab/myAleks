def check_and_consume_student_plan(quiz_record_id, student_id):
    try:
        quiz_record = QuizRecord.objects.get(pk = quiz_record_id)
    except:
        return {'status': False, 'reason': 'quiz not existed'}

    try:
        student_plan = StudentPlan.objects.get(student=student_id, cls=quiz_record.cls)
    except:
        return {'status': False, 'reason': 'student plan not existed'}


    if student_plan.paid == False:
        return {'status': False, 'reason': 'student plan not paid'}

    quiz_type = quiz_record.quiz.quiz_type
    resources = json.loads(student_plan.remaining_resouces)

    if quiz_type in resources and resources[quiz_type] > 0:
        resources[quiz_type] -= 1
        #TODO:
