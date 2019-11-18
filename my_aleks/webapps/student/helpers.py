from .models import *
from webapps.school.models import School, Cls

#消课
def reduce_cls(tuition_id):
    t = Tuition.objects.get(pk=tuition_id)
    if not t.paid or t.expired:
        return {'result': False, 'reason': 'tuition unpaid or expired'}

    if t.remaining_no <= 0:
        t.expired = True
        t.save()
        return {'result': False, 'reason': 'no remaining classes'}

    t.reamining_no -= 1
    if t.remaining_no <= 0:
        t.expired = True
        t.save()
    return {'result': True}

def create_tuition(student_id, total_fee, cls_id, remaining_no):
    try:
        student = StudentProfile.objects.get(pk=student_id)
    except:
        return {'status': False, 'reason': 'student not existed'}

    try:
        cls = Cls.objects.get(pk=cls_id)
    except:
        return {'status': False, 'reason': 'cls not existed'}
    
    t = Tuition(student=student, remaining_no=remaining_no, cls=cls, fee=total_fee)

    try:
        t.school = cls.school
    except:
        pass

    t.save()
    return {'status': True, 'tuition': t}

def pay_tuition(student_id, tuition_id):
    try:
        tuition = Tuition.objects.get(pk=tuition_id)
    except:
        return {'status': False, 'reason': 'tuition not existed'}

    tuition.paid = True
    tuition.save()

    return {'status': True}
