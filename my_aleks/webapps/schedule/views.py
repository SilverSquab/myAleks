from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from webapps.school.models import *
from .models import *
import json
import datetime
import time
import traceback
from django.db import transaction
# Create your views here.

@login_required
@csrf_exempt
def ajax_add_schedule_event(request):
    user = request.user
    if request.method == "POST":
        #body = json.loads(request.body.decode('utf-8'))
        start = request.POST.get('start','')
        end = request.POST.get('end','')
        title = request.POST.get('title','')
        description = request.POST.get('description','')
        created_time = request.POST.get('created_time','')
        rule = request.POST.get('rule','')
        end_recurring_period = request.POST.get('end_recurring_period','')
        cls_id = request.POST.get('cls_id','')
        weekday = request.POST.get('weekday','')
        
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        created_time = datetime.datetime.strptime(created_time, "%Y-%m-%d")
        end_recurring_period = datetime.datetime.strptime(end_recurring_period, "%Y-%m-%d")

        cls = Cls.objects.get(pk=cls_id)
        if user.groups.filter(name='SCHOOL_MANAGER').exists():
            school = user.school
        elif user.groups.filter(name='TEACHER').exists():
            school = user.teacherprofile.school
        schedule_event = ScheduleEvent(start=start, end=end, title=title, description=description, created_time=created_time, rule=rule, end_recurring_period=end_recurring_period, cls=cls, school=school, weekday=weekday)
        #转化python和js的周几表示不同的问题
        if weekday == 0:
            weekday = 6
        else:
            weekday = int(weekday) - 1
        one_day = datetime.timedelta(days=1)
        start1 = datetime.timedelta(hours=start.hour, minutes=start.minute)
        end1 = datetime.timedelta(hours=end.hour, minutes=end.minute)
        start_list = []
        end_list = []
        while(True):
            if created_time == end_recurring_period:
                break
            if created_time.weekday() == weekday:
                c = created_time + start1
                f = created_time + end1
                start_list.append(c)
                end_list.append(f)
            created_time = created_time + one_day
        #保存原型和事件发生
        try:
            with transaction.atomic():
                schedule_event.save()
                for index in range(len(start_list)):
                    occurrence = ScheduleOccurrence.objects.create(title=schedule_event.title,description=schedule_event.description,start=start_list[index],end=end_list[index],event=schedule_event,teacher=cls.teacher,original_start=schedule_event.start,original_end=schedule_event.end,cls=cls)
                    occurrence.save()
        except (Exception, BaseException) as e:
            traceback.print_exc()
            return HttpResponse('save plan failed')

        return HttpResponse(json.dumps({'status':'OK','id':schedule_event.pk}))
    return HttpResponse('error method')

@login_required
@csrf_exempt
def ajax_get_schedule_event_by_class(request):
    user = request.user
    if request.method == "POST":
        cls_id = request.POST.get('cls_id','')
        created_time = request.POST.get('created_time','')
        end_recurring_period = request.POST.get('end_recurring_period','')


        datetime.datetime.strptime(created_time, "%Y-%m-%d")
        datetime.datetime.strptime(end_recurring_period, "%Y-%m-%d")


        schedule_events = ScheduleEvent.objects.filter(cls__id=cls_id, created_time__gte=created_time, end_recurring_period__lte = end_recurring_period)
        event_list = []
        for schedule_event in schedule_events:
            event_list.append({'id':schedule_event.id,'start':schedule_event.start.strftime("%Y-%m-%d %H:%M:%S"), 'end': schedule_event.end.strftime("%Y-%m-%d %H:%M:%S"), 
                            'title':schedule_event.title, 
                            'description':schedule_event.description})
        return HttpResponse(json.dumps(event_list))
    return HttpResponse('error method')


@login_required
@csrf_exempt
def ajax_get_schedule_by_school(request):
    user = request.user
    if request.method == "POST":
        cls_id = request.POST.get('cls_id','')
        if user.groups.filter(name='SCHOOL_MANAGER').exists():
            school = user.school
        else:
            return HttpResponse('user not school')
        schedule_events = ScheduleEvent.objects.filter(cls_id=cls_id,school_id=school.pk)
        event_list = []
        eightHour = datetime.timedelta(hours=8)
        for schedule_event in schedule_events:
            start = schedule_event.start + eightHour
            end = schedule_event.end + eightHour
            created_time = schedule_event.created_time + eightHour
            end_recurring_period = schedule_event.end_recurring_period + eightHour
            event_list.append({'id':schedule_event.id,'start':start.strftime("%Y-%m-%d %H:%M:%S"),'end': end.strftime("%Y-%m-%d %H:%M:%S"),'title':schedule_event.title,'description':schedule_event.description,'end_recurring_period':end_recurring_period.strftime("%Y-%m-%d"),'created_time':created_time.strftime("%Y-%m-%d")})
        return HttpResponse(json.dumps(event_list))
    return HttpResponse('error method')
        
@login_required
@csrf_exempt
def ajax_delete_schedule_by_id(request):
    user = request.user
    if request.method == "GET":
        schedule_id = request.GET.get('schedule_id',-1)
        if schedule_id != -1:
            try:
                ScheduleEvent.objects.filter(pk = schedule_id).delete()
                return HttpResponse('OK')
            except:
                return HttpResponse('delete error')
        return HttpResponse('schedule_id not null')
    return HttpResponse('error method')


@login_required
@csrf_exempt
def ajax_update_schedule_event(request):
    user = request.user
    if request.method == "POST":
        #获取请求数据和判断
        created_time = request.POST.get('created_time','')
        end_recurring_period = request.POST.get('end_recurring_period','')
        title = request.POST.get('title','')
        description = request.POST.get('description','')
        id = request.POST.get('id',-1)
        if id == -1:
            return HttpResponse('id is null')
        #预处理数据
        try:
            schedule = ScheduleEvent.objects.get(pk = id)
        except:
            return HttpResponse('id is null')
        end_recurring_period = datetime.datetime.strptime(end_recurring_period, "%Y-%m-%d")
        created_time = datetime.datetime.strptime(created_time, "%Y-%m-%d")
        #cls = schedule.cls
        try:
            created_date = created_time.date()
            end_date = end_recurring_period.date()
            schedule_created_date = schedule.created_time.date()+datetime.timedelta(days=1)
            schedule_end_date = schedule.end_recurring_period.date()+datetime.timedelta(days=1)
            with transaction.atomic():
                if created_date < schedule_created_date:
                    create_occurrence(schedule,created_date,schedule_created_date)
                elif created_date > schedule_created_date:
                    ScheduleOccurrence.objects.filter(event = schedule,end__lte=created_time).delete()
                if end_date > schedule_end_date:
                    create_occurrence(schedule,schedule_end_date,end_date)
                elif end_date < schedule_end_date:
                    ScheduleOccurrence.objects.filter(event = schedule,start__gte=end_recurring_period).delete()
                schedule.title = title
                schedule.created_time = created_time
                schedule.description = description
                schedule.end_recurring_period = end_recurring_period
                schedule.save()
                ScheduleOccurrence.objects.filter(event = schedule).update(title=schedule.title,description=schedule.description)

        except (Exception, BaseException) as e:
            traceback.print_exc()
            return HttpResponse('save plan failed')
        return HttpResponse('OK')
    return HttpResponse('error method')


def create_occurrence(schedule,created_time,end_recurring_period):
    weekday = schedule.weekday
    #转化python和js的周几表示不同的问题
    if weekday == 0:
        weekday = 6
    else:
        weekday = int(weekday) - 1
    one_day = datetime.timedelta(days=1)
    eightHour = datetime.timedelta(hours=8)
    start1 = schedule.start + eightHour
    end1 = schedule.end + eightHour
    start_list = []
    end_list = []
    while(True):
        if created_time >= end_recurring_period:
            break
        if created_time.weekday() == weekday:
            c = datetime.datetime(created_time.year,created_time.month,created_time.day,start1.hour,start1.minute)
            f = datetime.datetime(created_time.year,created_time.month,created_time.day,end1.hour,end1.minute)
            start_list.append(c)
            end_list.append(f)
        created_time = created_time + one_day
    #保存原型和事件发生
    for index in range(len(start_list)):
        occurrence = ScheduleOccurrence.objects.create(description=schedule.description,start=start_list[index],end=end_list[index],event=schedule,teacher=schedule.cls.teacher,original_start=schedule.start,original_end=schedule.end,title=schedule.title,cls=schedule.cls)
        occurrence.save()
    return "OK"




@login_required
@csrf_exempt
def ajax_get_schedule_occurrence_by_class(request):
    user = request.user
    if request.method == "POST":
        cls_id = request.POST.get('cls_id',-1)
        if cls_id == -1:
            return HttpResponse('cls_id is null')
        start = request.POST.get('start','')
        end = request.POST.get('end','')

        start = datetime.datetime.strptime(start,'%Y-%m-%d')
        end = datetime.datetime.strptime(end,'%Y-%m-%d')
        eightHour = datetime.timedelta(hours=8)
        try:
            teacher = Cls.objects.get(pk = cls_id).teacher
        except:
            return HttpResponse('teacher/cls get null')
        occurrences = ScheduleOccurrence.objects.filter(teacher=teacher,start__gte=start,end__lte=end)
        occurrence_list = []
        for occurrence in occurrences:
            start1 = occurrence.start + eightHour
            end1 = occurrence.end + eightHour
            occurrence_list.append({'id':occurrence.id,'start':start1.strftime("%Y-%m-%d %H:%M:%S"),'end':end1.strftime("%Y-%m-%d %H:%M:%S"),'title':occurrence.title,'description':occurrence.description});
        return HttpResponse(json.dumps(occurrence_list))
    return HttpResponse('method error')



@login_required
@csrf_exempt
def ajax_add_schedule_occurrence(request):
    if request.method == "POST":
        cls_id = request.POST.get('cls_id',-1)
        if cls_id == -1:
            return HttpResponse('cls_id is null')
        start = request.POST.get('start','')
        end = request.POST.get('end','')
        title = request.POST.get('title','')
        description = request.POST.get('description','')
        try:
            cls = Cls.objects.get(pk=cls_id)
        except:
            return HttpResponse('cls not find')
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        occurrence = ScheduleOccurrence.objects.create(description=description,start=start,end=end,teacher=cls.teacher,title=title,cls=cls)
        return HttpResponse(json.dumps({'status':'OK','id':occurrence.pk}))
    return HttpResponse('method error')

@login_required
@csrf_exempt
def ajax_update_schedule_occurrence(request):
    if request.method == "POST":
        id = request.POST.get('id',-1)
        if id == -1:
            return HttpResponse('id is null')
        title = request.POST.get('title','')
        description = request.POST.get('description','')
        start = request.POST.get('start','')
        end = request.POST.get('end','')
        try:
            occurrence = ScheduleOccurrence.objects.get(pk=id)
        except:
            return HttpResponse('occurrence not find')
        if title:
            occurrence.title = title
        if description:
            occurrence.description = description
        if start:
            start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            occurrence.start = start
        if end:
            end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            occurrence.end = end
        occurrence.save()
        return HttpResponse('OK')
    return HttpResponse('method error')


@login_required
@csrf_exempt
def ajax_delete_schedule_occurrence(request):
    if request.method == "GET":
        id = request.GET.get('occurrence_id',-1)
        if id == -1:
            return HttpResponse('id is null')
        try:
            occurrence = ScheduleOccurrence.objects.get(pk=id).delete()
            return HttpResponse('OK')
        except:
            return HttpResponse('delete error')
    return HttpResponse('method error')

















