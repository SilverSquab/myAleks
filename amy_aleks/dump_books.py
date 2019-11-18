from webapps.textbook.models import *

ts = Textbook.objects.all()

for t in ts:
  print(t.subject, t.publisher, t.name, t.id)
  cs = t.chapters.all()
  for c in cs: 
    print('\t', c.order, c.name, c.id)
    ss = c.sections.all()
    for s in ss:
      print('\t\t', s.order, s.name, s.id)
      ps = s.parts.all()
      for p in ps:
        print('\t\t\t', p.order, p.name, p.id)


