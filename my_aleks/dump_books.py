from webapps.textbook.models import *

for t in ts:
  print(t.subject, t.publisher, t.name, t.id)
  cs = t.chapter_set.all()
  for c in cs: 
    print('\t', c.order, c.name, c.id)
    ss = c.section_set.all()
      for s in ss:
        print('\t\t', s.order, s.name, s.id)
        ps = s.part_set.all()
          for p in ps:
            print('\t\t\t', p.order, p.name, p.id)


