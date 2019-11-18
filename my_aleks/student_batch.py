from django.contrib.auth.models import User, Group
from webapps.student.models import StudentProfile
import json
from webapps.school.models import Cls

def csv_to_list(fname):
    student_list = []
    f = open(fname)
    while True:
        line = f.readline()
        print(line)
        if not line:
        	break
        l = line.split(',')
        d = {}
        d['grade'] = int(l[0])
        d['name'] = l[2]
        d['info'] = str(l[1]) + ' ' + l[3]
        student_list.append(d)
        
    return student_list

#start_index: if a school has multiple batches, start_index is used to track how many students it already has
def batch_students(school_name, students_list, start_index = 0, cls_id = 0):
    group = Group.objects.get(name='STUDENT')
    length = len(students_list)
    i = start_index
    profile_list = []
    print(students_list)
    for student in students_list:
        print(student)
        u = User.objects.create(username=school_name + str(i))
        u.groups.add(group)
        u.save()
        profile = StudentProfile.objects.create(user=u, info=student['info'], grade=student['grade'], name=student['name'])
        profile.age = student['grade'] + 6
        profile.save()
        profile.student_no = profile.pk + 100000
        profile.save()
        profile_list.append(profile)
        i += 1
        
    if cls_id != 0:
        cls = Cls.objects.get(pk=cls_id)
        students = json.loads(cls.students)
        student_no_list = []
        for student in profile_list:
            print(student)
            student_no_list.append(str(student.student_no))
            print(json.dumps([str(cls_id)]))
            student.cls_list = json.dumps([str(cls_id)])
            student.save()
        students = json.loads(cls.students)
        students += student_no_list
        cls.students = json.dumps(students)
        cls.num = len(students)
        cls.save()
