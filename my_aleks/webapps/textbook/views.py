from django.shortcuts import render
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .helpers import *
import json

# Create your views here.

def ajax_upload_textbook(request):
    dic = request.POST
    chinese_name = dic['chinese_name']
    try:
        textbook = Textbook.objects.get(chinese_name=chinese_name)
        return HttpResponse('already existed')
    except:
        pass
    if dic.has_key('publisher'):
        try:
            publisher = Publisher.objects.get(id=dic['publisher'])
        except:
            return HttpResponse('publisher not exited')

@csrf_exempt
def ajax_upload_textbooks(request):
    publisher = Publisher.objects.get(name='BEISHIDAXIN')
    dic = json.loads(request.body.decode('utf-8'))
    create_whole_textbook(dic, publisher)

    return HttpResponse('OK')

@login_required
def ajax_get_all_textbooks(request):
    ts = Textbook.objects.all()
    l = list(ts.values('id', 'grade_no', 'subject', 'name', 'chinese_name', 'grade', 'publisher','order'))
    return HttpResponse(json.dumps(l))

@login_required
def ajax_get_textbook_structure(request):
    book_id = request.GET.get('book_id', '')
    if not book_id:
        return HttpResponse('failed: missing book id')

    try:
        book = Textbook.objects.get(pk=book_id)
    except:
        return HttpResponse('failed: book not found')

    dic = model_to_dict(book)
    dic['id'] = book.id
    dic['chapters'] = []

    for chapter in book.chapters.all():
        chapter_dic = model_to_dict(chapter)
        chapter_dic['sections'] = []
        chapter_dic['id'] = chapter.id
        
        for section in chapter.sections.all():
            section_dic = model_to_dict(section)
            section_dic['parts'] = []
            section_dic['id'] = section.id

            for part in section.parts.all():
                part_dic = model_to_dict(part)
                part_dic['id'] = part.id
                section_dic['parts'].append(part_dic)
            chapter_dic['sections'].append(section_dic)

        dic['chapters'].append(chapter_dic)
        

    return HttpResponse(json.dumps(dic))
