from webapps.textbook.models import Section
import json


#upload nodes list to sections in a whole book

def func(filename):
    f = open(filename)
    while True:
        line = f.readline()
        if not line:
            break

        words_list = line.split()
        if len(words_list) > 0:
            if len(words_list[-1]) > 20:
                nodes_line = f.readline()
                nodes = nodes_line.split()
                
                try:
                    section = Section.objects.get(pk = words_list[-1])
                    section.nodes_list = json.dumps(nodes)
                    section.save()
                except:
                    print('not found section ' + words_list[-1])


        
