#coding=utf-8
from django.http import HttpResponse
import re
from django.db import connection, transaction
from django.template import Context,loader
from django.conf import settings
from tools.util import *
from datetime import *
import json
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TITLE={"click_rate":"点击率",
"first_click_time":"第一次点击的时间间隔",
"non_click_rate":"搜索无点击率",
"page_change_insearch_rate":"一次搜索内的翻页率",
"page_change_rate":"翻页率",
"pos1_click_rate":"第一位点击率",
"pos2_click_rate":"第二位点击率",
"pos3_click_rate":"第三位点击率",
"top3_click_rate":"前三位点击率",
"query_change_rate":"QUERY更改率",
"total_click":"总点击次数",
"total_search":"总搜索次数"}

def get_key_list():
  cursor = connection.cursor()
  sql="SELECT * FROM `keys`"
  cursor.execute(sql)
  result=dictfetchall(cursor)
  key_list=[]
  for key in result:
    key_list.append({"key_name":key['key_name'],"key_title":get_title(key['key_name'])})
  key_list.sort()
  return key_list

def index (request):
    during=[]
    end = datetime.now()
    for i in range(0,10):
      tmp_date=end-timedelta(i)
      during.append(str(tmp_date).split(' ')[0])

    click_result={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    search_result={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    date_range=set()
    cursor = connection.cursor()
    #sql="SELECT * FROM day_total_click WHERE timestamp >= '%s' order by timestamp asc " %(during[-1])
    sql="SELECT a.*,b.* FROM item_day_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='total_click' and a.timestamp >= '%s' order by a.timestamp asc " % (during[-1])

    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])
        if i['engine']=='baidu':
          click_result['baidu'].append(int(i['value']))
        elif i['engine']=='google':
          click_result['google'].append(int(i['value']))
        elif i['engine']=='onebox':
          click_result['onebox'].append(int(i['value']))
        elif i['engine']=='qss':
          click_result['qss'].append(int(i['value']))
        elif i['engine']=='other':
          click_result['other'].append(int(i['value']))
    sql="SELECT a.*,b.* FROM item_day_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='total_search' and a.timestamp >= '%s' order by a.timestamp asc " % (during[-1])

    print sql
    during.sort()
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])
        if i['engine']=='baidu':
          search_result['baidu'].append(int(i['value']))
        elif i['engine']=='google':
          search_result['google'].append(int(i['value']))
        elif i['engine']=='onebox':
          search_result['onebox'].append(int(i['value']))
        elif i['engine']=='qss':
          search_result['qss'].append(int(i['value']))
        elif i['engine']=='other':
          search_result['other'].append(int(i['value']))

    current_datetime="%s -> %s"%(str(end-timedelta(10)).split(' ')[0],str(end).split(' ')[0])
    date_range=list(date_range)
    date_range.sort()
    template = loader.get_template('index.html')
    key_list=get_key_list()
    params= Context({"key_list":key_list,"during":date_range,"current_datetime":current_datetime,"click_result":click_result,"search_result":search_result})
    
    
    return HttpResponse(template.render(params))

def get_click_and_search_amounts(request):
      
    time_from=request.GET['from']
    time_to=request.GET['to']
    date_range=set()
    during=[]
    time_from_part=time_from.split('-')
    time_to_part=time_to.split('-')

    start = date(int(time_from_part[0]),int(time_from_part[1]),int(time_from_part[2]))
    end = date(int(time_to_part[0]),int(time_to_part[1]),int(time_to_part[2]))
    
    total_days= (end-start).days
    for i in range(0,(end-start).days+1):
      tmp_date=end-timedelta(i)
      during.append(str(tmp_date)[5:])
    

    click_result={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    search_result={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    
    cursor = connection.cursor()
    sql="SELECT a.*,b.* FROM item_day_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='total_click' and a.timestamp >= '%s' and a.timestamp<='%s' order by a.timestamp asc " % (time_from,time_to)

    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])
        if i['engine']=='baidu':
          click_result['baidu'].append(int(i['value']))
        elif i['engine']=='google':
          click_result['google'].append(int(i['value']))
        elif i['engine']=='onebox':
          click_result['onebox'].append(int(i['value']))
        elif i['engine']=='qss':
          click_result['qss'].append(int(i['value']))
        elif i['engine']=='other':
          click_result['other'].append(int(i['value']))

    sql="SELECT a.*,b.* FROM item_day_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='total_search' and a.timestamp >= '%s' and a.timestamp<='%s' order by a.timestamp asc " % (time_from,time_to)

    print sql
    during.sort()
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])

        if i['engine']=='baidu':
          search_result['baidu'].append(int(i['value']))
        elif i['engine']=='google':
          search_result['google'].append(int(i['value']))
        elif i['engine']=='onebox':
          search_result['onebox'].append(int(i['value']))
        elif i['engine']=='qss':
          search_result['qss'].append(int(i['value']))
        elif i['engine']=='other':
          search_result['other'].append(int(i['value']))

    date_range=list(date_range)
    date_range.sort()
    params= {"click_result":click_result,"search_result":search_result,"during":date_range}
    return HttpResponse(json.dumps(params))



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


def page (request):
    during=[]
    end = datetime.now()
    for i in range(0,10):
      tmp_date=end-timedelta(i)
      during.append(str(tmp_date).split(' ')[0])
    
    key_name=request.GET['key']

    return_dict={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    date_range=set()
    cursor = connection.cursor()
    
    sql="SELECT a.*,b.* FROM item_day_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='%s' and a.timestamp >= '%s' order by a.timestamp asc " % (key_name,during[-1])

    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])
        if i['engine']=='baidu':
          return_dict['baidu'].append(float(i['value']))
        elif i['engine']=='google':
          return_dict['google'].append(float(i['value']))
        elif i['engine']=='onebox':
          return_dict['onebox'].append(float(i['value']))
        elif i['engine']=='qss':
          return_dict['qss'].append(float(i['value']))
        elif i['engine']=='other':
          return_dict['other'].append(float(i['value']))

    return_hour_dict={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    date_range_hour=set()
    sql="SELECT a.*,b.* FROM item_hour_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='%s' and a.timestamp >= '%s' order by a.timestamp asc " % (key_name,datetime.now()-timedelta(hours=7))

    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range_hour.add(str(i['timestamp']).split(' ')[1])
        if i['engine']=='baidu':
          return_hour_dict['baidu'].append(float(i['value']))
        elif i['engine']=='google':
          return_hour_dict['google'].append(float(i['value']))
        elif i['engine']=='onebox':
          return_hour_dict['onebox'].append(float(i['value']))
        elif i['engine']=='qss':
          return_hour_dict['qss'].append(float(i['value']))
        elif i['engine']=='other':
          return_hour_dict['other'].append(float(i['value']))



    current_datetime="%s -> %s"%(str(end-timedelta(10)).split(' ')[0],str(end).split(' ')[0])
    date_range=list(date_range)
    date_range.sort()
    
    date_range_hour=list(date_range_hour)
    date_range_hour.sort()

    key_list=get_key_list()
    title=get_title(key_name)
    template = loader.get_template('page.html')
    params= Context({"return_hour_dict":return_hour_dict,"date_range_hour":date_range_hour,"key_list":key_list,"title":title,"key_name":key_name,"during":date_range,"current_datetime":current_datetime,"return_dict":return_dict})
    
    return HttpResponse(template.render(params))

def get_page(request):
    key_name=request.GET['key']
    time_from=request.GET['from']
    time_to=request.GET['to']
    date_range=set()
    during=[]
    time_from_part=time_from.split('-')
    time_to_part=time_to.split('-')

    start = date(int(time_from_part[0]),int(time_from_part[1]),int(time_from_part[2]))
    end = date(int(time_to_part[0]),int(time_to_part[1]),int(time_to_part[2]))
    
    total_days= (end-start).days
    for i in range(0,(end-start).days+1):
      tmp_date=end-timedelta(i)
      during.append(str(tmp_date)[5:])
    
    
    return_dict={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    
    cursor = connection.cursor()
    sql="SELECT a.*,b.* FROM item_day_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='%s' and a.timestamp >= '%s' and a.timestamp<='%s' order by a.timestamp asc " % (key_name,time_from,time_to)
    
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])
        if i['engine']=='baidu':
          return_dict['baidu'].append(float(i['value']))
        elif i['engine']=='google':
          return_dict['google'].append(float(i['value']))
        elif i['engine']=='onebox':
          return_dict['onebox'].append(float(i['value']))
        elif i['engine']=='qss':
          return_dict['qss'].append(float(i['value']))
        elif i['engine']=='other':
          return_dict['other'].append(float(i['value']))

    date_range=list(date_range)
    date_range.sort()
    params= {"return_dict":return_dict,"during":date_range}
    return HttpResponse(json.dumps(params))



def get_title(key_name):
  if key_name in TITLE:
    return TITLE[key_name]
  else:
    return key_name.upper().replace('_',' ')



def get_hour_data(request):
    key_name=request.GET['key']
    time_from=request.GET['from']
    time_to=request.GET['to']
    date_range=set()
    during=[]
    time_prefix=str(datetime.now()).split(' ')[0]+' '
    time_from_part=time_prefix+time_from.split(':')[0]+':00'
    time_to_part=time_prefix+time_to.split(':')[0]+':00'

    

    for i in range(int(time_from.split(':')[0]),int(time_to.split(':')[0])+1):
      if i <10:
        during.append('0'+str(i)+':00')
      else:
        during.append(str(i)+':00')
    return_dict={"baidu":[],"google":[],"qss":[],"other":[],"onebox":[]}
    
    cursor = connection.cursor()
    sql="SELECT a.*,b.* FROM item_hour_values a LEFT JOIN `keys` b ON a.key_id=b.id WHERE b.key_name='%s' and a.timestamp >= '%s' and a.timestamp<='%s' order by a.timestamp asc " % (key_name,time_from_part,time_to_part)
    
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    for i in result:
        date_range.add(str(i['timestamp']).split(' ')[0][5:])
        if i['engine']=='baidu':
          return_dict['baidu'].append(float(i['value']))
        elif i['engine']=='google':
          return_dict['google'].append(float(i['value']))
        elif i['engine']=='onebox':
          return_dict['onebox'].append(float(i['value']))
        elif i['engine']=='qss':
          return_dict['qss'].append(float(i['value']))
        elif i['engine']=='other':
          return_dict['other'].append(float(i['value']))

    date_range=list(date_range)
    date_range.sort()
    params= {"return_dict":return_dict,"during":date_range}
    return HttpResponse(json.dumps(params))



