#coding=utf-8
from django.http import HttpResponse
import re
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from clientinfo.models import *
from django.template import Context,loader
from django.conf import settings
from datetime import *
import json
from tools.util import dictfetchall

#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import connection, transaction


@login_required
def index (request):
    username=None
    if request.user.is_authenticated():
        username=request.user.username
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  

    template = loader.get_template('clientinfo.html')
    params= Context({"username":username})
    return HttpResponse(template.render(params))

@login_required
def setup_amounts(request):
    username=None
    if request.user.is_authenticated():
        username=request.user.username
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    
    during=[]
    end = datetime.now()
    for i in range(0,7):
      tmp_date=end-timedelta(i)
      during.append(str(tmp_date).split(' ')[0][5:])
    
    cursor = connection.cursor()
    sql="SELECT * FROM  client_amount WHERE date >= '%s' order by date desc limit 0,50  " % ('2012-'+during[-1])
    print sql
    during.sort()
    cursor.execute(sql)
    result=dictfetchall(cursor)     
    weibo=[]
    sem=[]
    seo=[]
    for i in result:
        if i['client_type']==2:
          seo.append(int(i['amount']))
        elif i['client_type']==1:
          sem.append(int(i['amount']))
        elif i['client_type']==0:
          weibo.append(int(i['amount']))
    current_datetime="%s -> %s"%(str(end-timedelta(6)).split(' ')[0],str(end).split(' ')[0])
    
    
    after_range_num = 3
    befor_range_num = 4


    try:
      page = int(request.GET.get("page",1))
      if page < 1:
        page = 1
    except ValueError:
      page = 1
    paginator = Paginator(result,50)
    try:
      search_result = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
      search_result = paginator.page(paginator.num_pages)
    if page >= after_range_num:
      page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
    else:
      page_range = paginator.page_range[0:int(page)+befor_range_num]    

    template = loader.get_template('clientinfo_setup_amounts.html')
    print weibo,sem,seo
    params= Context({'page_range':page_range,"current_datetime":current_datetime,"result_list":search_result,"result":{"weibo":weibo,"sem":sem,"seo":seo,"during":during},"username":username})
    
    
    return HttpResponse(template.render(params))


@login_required
def get_setup_amounts(request):
    
    time_from=request.GET['from']
    time_to=request.GET['to']
    
    during=[]
    time_from_part=time_from.split('-')
    time_to_part=time_to.split('-')

    start = date(int(time_from_part[0]),int(time_from_part[1]),int(time_from_part[2]))
    end = date(int(time_to_part[0]),int(time_to_part[1]),int(time_to_part[2]))
    
    total_days= (end-start).days
    for i in range(0,(end-start).days+1):
      tmp_date=end-timedelta(i)
      during.append(str(tmp_date)[5:])
    
    cursor = connection.cursor()
    sql="SELECT * FROM  client_amount WHERE date >= '%s' and date<='%s' ORDER BY date " % (time_from,time_to)
    print sql
    during.sort()
    cursor.execute(sql)
    result=dictfetchall(cursor) 
    weibo=[]
    sem=[]
    seo=[]
    for i in result:
        if i['client_type']==2:
          seo.append(int(i['amount']))
        elif i['client_type']==1:
          sem.append(int(i['amount']))
        elif i['client_type']==0:
          weibo.append(int(i['amount']))
    
    params= {"result":{"weibo":weibo,"sem":sem,"seo":seo,"during":during}}
    return HttpResponse(json.dumps(params))


from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
