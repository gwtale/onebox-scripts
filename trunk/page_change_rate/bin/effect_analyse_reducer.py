# -*- coding:utf-8 -*-

# top page change query
# @ericyue
# hi.moonlight@gmail.com

total_query={}
def merge(str1):
  global total_query
  str1=str1.rstrip("\n")
  items = str1.split("\t")
  query = items[0]
  search=int(items[1])
  page=int(items[2])
  if query not in total_query:
    total_query[query]={"search":0,"page":0,"rate":0.0}
  total_query[query]['search']+=search
  total_query[query]['page']+=page
    
if __name__=='__main__':
    while True :
      try:
        line = raw_input().rstrip('\n')
        merge(line)
      except EOFError:
        break
    for i in total_query:
      total_query[i]['rate']=total_query[i]['page']/float(total_query[i]['search'])
      total_query[i]['avg']=(2*float(total_query[i]['page'])*float(total_query[i]['search']))/(float(total_query[i]['search'])+float(total_query[i]['page']))
    total_query=sorted(total_query.iteritems(), key=lambda x:(-x[1]['avg']))
    for i in total_query:
      print "%s\t%s\t%s\t%s" % (i[0],i[1]['avg'],i[1]['rate'],i[1]['search'])
