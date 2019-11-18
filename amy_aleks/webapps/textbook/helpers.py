from .models import *

def create_textbook(dic, publisher):
    textbook = Textbook.objects.get_or_create(**dic)[0]
    textbook.publisher = publisher
    textbook.save()
    return textbook

def create_chapter(dic, textbook):
    chapter = Chapter.objects.get_or_create(**dic)[0]
    chapter.textbook = textbook
    chapter.save()
    return chapter

def create_section(dic, chapter):
    section = Section.objects.get_or_create(**dic)[0]
    section.chapter = chapter
    section.save()
    return section

def create_part(dic, section):
    part = Part.objects.get_or_create(**dic)[0]
    part.section = section
    part.save()
    return part

def create_whole_textbook(dic, publisher):
    attrs = dic['attrs']
    textbook = create_textbook(attrs, publisher)
    for chapter in dic['chapters']:
        c = create_chapter(chapter['attrs'], textbook)
        print(c)
        print('\n')
        for section in chapter['sections']:
            s = create_section(section['attrs'], c)
            print(s)
            for part in section['parts']:
                p = create_part(part['attrs'], s)
