#coding=utf-8
from django.http import HttpResponse
import re
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from clientinfo.models import *
from django.template import Context,loader
from django.conf import settings
from tools.util import *
from datetime import *
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@login_required
def index (request):
    username=None
    if request.user.is_authenticated():
        username=request.user.username
    
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    
    cursor = connection.cursor()
    sql="SELECT * FROM  t_user_info "
    cursor.execute(sql)
    result_list=dictfetchall(cursor)

    weibo={"try":0,"normal":0,"crack":0,"stop":0}
    seo={"try":0,"normal":0,"crack":0,"stop":0}
    sem={"try":0,"normal":0,"crack":0,"stop":0}


    for i in result_list:
        if i['c_type']==0:
          if i['c_count_state']==0:
            weibo['try']+=1
          elif  i['c_count_state']==1:
             weibo['normal']+=1
          elif  i['c_count_state']==-1:
             weibo['stop']+=1
          elif  i['c_count_state']==-2:
             weibo['crack']+=1
        if i['c_type']==2:
          if i['c_count_state']==0:
            seo['try']+=1
          elif  i['c_count_state']==1:
             seo['normal']+=1
          elif  i['c_count_state']==-1:
             seo['stop']+=1
          elif  i['c_count_state']==-2:
             seo['crack']+=1
        if i['c_type']==1:
          if i['c_count_state']==0:
            sem['try']+=1
          elif  i['c_count_state']==1:
             sem['normal']+=1
          elif  i['c_count_state']==-1:
             sem['stop']+=1
          elif  i['c_count_state']==-2:
             sem['crack']+=1

    mweibo=0
    mseo=0
    msem=0
    current_date=datetime.now()
    print str(current_date)
    week_list=[]
    money_result_list=[]

    for i in range(5):
      week_list.append(str(current_date-timedelta(7*i))+'='+str(current_date-timedelta(7*i+6)))
    week_list.reverse()
    for i in week_list:
      sql="select a.*,b.c_type from t_finance_info a LEFT JOIN t_user_info b ON b.c_user_id=a.c_user_id where a.c_pay_time>='%s' and a.c_pay_time<='%s' " %(i.split('=')[1],i.split('=')[0])
      print sql
      cursor.execute(sql)
      money_result_list.append(dictfetchall(cursor))
    money_result={"weibo":[],"seo":[],"sem":[],"total":[]}
    print money_result_list
    
    for week in money_result_list:
      #每循环是一个周
      w_weibo=0.0
      w_seo=0.0
      w_sem=0.0
      for f in week:
        if f['c_type']==0:
          w_weibo+=int(f['c_pay_amount'])
        elif f['c_type']==2:
          w_seo+=int(f['c_pay_amount'])
        elif f['c_type']==1:
          w_sem+=int(f['c_pay_amount'])

      money_result['weibo'].append(w_weibo)
      money_result['seo'].append(w_seo)
      money_result['sem'].append(w_sem)
      money_result['total'].append(w_sem+w_weibo+w_seo)

    print money_result
    template = loader.get_template('index.html')
    params= Context({"money":money_result,"weibo":weibo,"seo":seo,"sem":sem,"username":username})
      
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
