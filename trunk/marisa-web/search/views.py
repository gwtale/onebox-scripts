#coding=utf-8
from django.http import HttpResponse
import re
from django.db import connection, transaction
from django.template import Context,loader
from django.conf import settings
from datetime import *
from memcached import memcache
import xapian
import sys
import string
import time
import os
from xapian import MultiValueSorter
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
databasePath = os.path.abspath('index_compressed')
FREQ=1
CLICK = 2
DATE=3
cache = memcache.Client(['127.0.0.1:11211'],debug=0)
def cut_str(str,length):
    is_encode = False
    try:
        str_encode = str.encode('gb18030')
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                str = str_encode.decode('gb18030') + '...'
            except:
                str_encode = str_encode[:-1]
                try:
                    str = str_encode.decode('gb18030') + '...'
                except:
                    is_encode = False
    if not is_encode:
        if length < len(str):
            length = length - 2
            return str[:length] + '...'
    return str

def search_database(keywords,result_limit,limit):
    c_key=('query_'+keywords+str(result_limit)).encode('utf-8')
    CT=cache.get(c_key)
    if CT!=None:
      print "using cache",c_key
      return CT
    database = xapian.Database(databasePath)
    enquire = xapian.Enquire(database)
    queryParser = xapian.QueryParser()
    queryParser.set_stemmer(xapian.Stem('english'))
    queryParser.set_database(database)
    queryParser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = queryParser.parse_query(keywords)
    rex=re.compile(r'[0-9]+|[a-zA-Z]+|[\x80-\xff3]{3}')
    all_terms=rex.findall(keywords.encode('utf-8'))  
    query_list = [] 
    for word in all_terms:
      query = xapian.Query(word)
      query_list.append(query)
    if len(query_list) != 1:
      query = xapian.Query(xapian.Query.OP_AND, query_list)
    else:
      query = query_list[0]

    offset= 0
    sorter = MultiValueSorter()
    sorter.add(1)
    sorter.add(2)
    enquire.set_query(query)
    enquire.set_sort_by_key(sorter)
    result_list=[]
    result_got=0
    max_try=0
    

    while True:
      print "loop",result_got
      print "limit",result_limit
      matches = enquire.get_mset(offset, limit)
      for match in matches:
        str_content=match.document.get_data()
        if str_content.find(keywords)==-1:
          continue
        query_content=cut_str(str_content,50)
        result_got+=1
        result_list.append({"index":result_got,"query":query_content,"freq":xapian.sortable_unserialise(match.document.get_value(FREQ)),"click":xapian.sortable_unserialise(match.document.get_value(CLICK)),"date":match.document.get_value(DATE)})
      offset+=limit
      max_try+=1
      if result_got>result_limit:
        break
      if max_try>15:
        break
    print cache.set(c_key,[result_list,result_got],3600)
    print "cached",c_key
    return result_list,result_got

def index (request):
    username=None
    if request.user.is_authenticated():
        username=request.user.username
    
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    
    offset=0
    limit=2000
    keywords=request.GET.get("keywords",None)
    
    try:
      result_limit=int(request.GET.get("limit",500))
    except:
      result_limit=500
    
    if not keywords :
      template = loader.get_template('index.html')    
      params= Context({"search_time":'0',"username":username})      
      return HttpResponse(template.render(params))
    try:
      page = int(request.GET.get("page",1))
      if page < 1:
        page = 1
    except ValueError:
      page = 1

    time_begin=time.time()
    return_data=search_database(keywords,result_limit,limit)
    result_list=return_data[0]
    result_got=return_data[1]
    time_end=time.time()
    current_url=request.path+'?keywords='+keywords
    after_range_num = 5
    befor_range_num = 9
    paginator = Paginator(result_list,200)
    try:
      search_result = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
      search_result = paginator.page(paginator.num_pages)
    
    if page >= after_range_num:
      page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
    else:
      page_range = paginator.page_range[0:int(page)+befor_range_num]    


    template = loader.get_template('index.html')
    params= Context({"keywords":keywords,"search_time":str(time_end-time_begin),"limit":result_limit,"result_size":result_got,"current_url":current_url,"username":username,'page_range':page_range,'result_list':search_result})
    return HttpResponse(template.render(params))

def unavailable (request):
    username=None
    if request.user.is_authenticated():
        username=request.user.username
    
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    
   
    template = loader.get_template('unavailable.html')
    params= Context({"username":username})
    return HttpResponse(template.render(params))
