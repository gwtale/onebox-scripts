#coding=utf-8
from django.http import HttpResponse
import re
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from clientinfo.models import *
from django.template import Context,loader
from django.conf import settings
import json
from tools.util import *
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from datetime import datetime,timedelta
#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@login_required
def index(request):
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
    sql="SELECT * FROM  client_amount WHERE date >= '%s' ORDER BY date " % ('2012-'+during[-1])
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

    template = loader.get_template('userinfo.html')
    params= Context({"result":{"weibo":weibo,"sem":sem,"seo":seo,"during":during},"username":username})
    return HttpResponse(template.render(params))
  

@login_required
def user_modify(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    
    try:
        uid=request.GET['uid']
    except:
        uid=None    
    
    cursor = connection.cursor()
    sql="SELECT * FROM  t_user_info WHERE c_user_id="+uid
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)
    


    template = loader.get_template('userinfo_modify_user.html')
    params= Context({"uid":uid,"username":username,"user":result[0]})
    return HttpResponse(template.render(params))

@login_required
def cash_modify(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
   
    try:
      uid=request.GET['uid']
    except:
      uid=None
    
    
    cursor = connection.cursor()
    sql="SELECT * FROM  t_user_info WHERE c_user_id="+uid
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)
    
    template = loader.get_template('userinfo_modify_cash.html')
    params= Context({"uid":uid,"username":username,"info":result[0]})
    return HttpResponse(template.render(params))

@login_required
def submit_modify_user(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    print request.GET['user_id']
    
    try:
      user_id=int(request.GET['user_id'])
    except:
      user_id=None
    try:
      client_type=int(request.GET['client_type'])
    except:
      client_type=None
    try:
      c_username=request.GET['username']
    except:
      c_username=None
    try:
      password=request.GET['password']
    except:
      password=None
    try:
      user_state=int(request.GET['user_state'])
    except:
      user_state=None
    try:
      expire_date_rd=request.GET['expire_date_rd']
      expire_date_rd+=' 00:00'
    except:
      expire_date_rd=None
  
    try:
      realname=request.GET['realname']
    except:
      realname=None
    try:
      company=request.GET['company']
    except:
      company=None
    try:
      email=request.GET['email']
    except:
      email=None
    try:
      idno=request.GET['idno']
    except:
      idno=None
    try:
      tel=request.GET['tel']
    except:
      tel=None



    if user_id == None:
      return HttpResponse(json.dumps({"status":"error"}))

    cursor = connection.cursor()
   
    sql="UPDATE t_user_info SET c_type=%s,c_user_name='%s',c_password='%s',c_count_state=%s,c_expired_time='%s',c_real_name='%s',c_company_name='%s',c_email_addr='%s',c_id_card_no='%s',c_phone_no='%s' WHERE c_user_id=%s" %(client_type,c_username,password,user_state,expire_date_rd,realname,company,email,idno,tel,user_id)
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)
    if cursor.rowcount==0:
      return HttpResponse(json.dumps({"status":"error"}))
    params= {"status":"ok"}
    return HttpResponse(json.dumps(params))



@login_required
def push_cash_modify(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  

    try:
      money=int(request.GET['money'])
    except:
      money=None
    try:
      user_id=int(request.GET['user_id'])
    except:
      user_id=None
    try:
      days=int(request.GET['days'])
    except:
      days=None

    if money==None or user_id == None or days ==None:
      return HttpResponse(json.dumps({"status":"error"}))
    
    
       
    cursor = connection.cursor()
    
    sql="INSERT INTO t_finance_info(c_user_id,c_pay_amount,c_expired_dates) values(%s,%s,%s) " % (user_id,money,days)
    print sql
    cursor.execute(sql)
    result=cursor.fetchall()
    if cursor.rowcount==0:
      return HttpResponse(json.dumps({"status":"error"}))

    sql="SELECT c_expired_time,c_count_state FROM t_user_info WHERE c_user_id=%s" % user_id
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor)


    expire_date=result[0]['c_expired_time']
    expire_date_today=datetime.now()
    if expire_date <expire_date_today:
      added_date=str(expire_date_today+timedelta(days))
    else:
      added_date=str(expire_date+timedelta(days))
    
    sql="UPDATE t_user_info SET c_expired_time='%s', c_count_state=1  WHERE c_user_id=%s" % (added_date,user_id)
    print sql
    cursor.execute(sql)
    result=cursor.fetchall()
    if cursor.rowcount==0:
      return HttpResponse(json.dumps({"status":"error"}))
    print result
    params= {"status":"ok","expire_date":str(added_date)}
    return HttpResponse(json.dumps(params))

@login_required
def get_user_info(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  

    try:
      user_id=int(request.GET['user_id'])
    except:
      user_id=None

    if user_id == None:
      return HttpResponse(json.dumps({"status":"error"}))

    cursor = connection.cursor()
   
    sql="SELECT * FROM t_user_info WHERE c_user_id=%s" % user_id

    cursor.execute(sql)
    result=dictfetchall(cursor)
    
    if len(result)<1:
        return HttpResponse(json.dumps({"status":"error"}))
    print result[0]
    if result[0]['c_type']==0:
        client_type='微博营销'
    elif result[0]['c_type']==1:
        client_type='SEO'
    elif result[0]['c_type']==2:
        client_type='SEM'

    user_state_list={0:"<option value=0>试用状态</option>",1:"<option value=1>正常状态</option>",-1:"<option value=-1>停用状态</option>",-2:"<option value=-2 >非法状态</option>"}
    user_state=''

    user_state+=user_state_list[result[0]['c_count_state']]
    for i in user_state_list:
      print i,result[0]['c_count_state']
      if i!=result[0]['c_count_state']:
        print user_state_list[i]

        user_state+=user_state_list[i]
    expire_date=str(result[0]['c_expired_time'])
    last_login=str(result[0]['c_last_login_time'])

    params= {"status":"ok","user":{"last_login":last_login,"expire_date":expire_date.split(' ')[0],"client_type":client_type,"username":result[0]['c_user_name'],"password":result[0]['c_password'],"user_state":user_state}}
    return HttpResponse(json.dumps(params))



@login_required
def paidinfo(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
        
    cursor = connection.cursor()
    sql="SELECT * FROM  t_user_info  "
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor) 
    weibo_paidinfo={"try":0,"normal":0,"stop":0,"crack":0}
    seo_paidinfo={"try":0,"normal":0,"stop":0,"crack":0}
    sem_paidinfo={"try":0,"normal":0,"stop":0,"crack":0}

    for i in result:
      if i['c_type']==0:
        if i['c_count_state']==0:
          weibo_paidinfo['try']+=1
        elif i['c_count_state']==1:
          weibo_paidinfo['normal']+=1
        elif i['c_count_state']==-1:
          weibo_paidinfo['stop']+=1
        elif i['c_count_state']==-2:
          weibo_paidinfo['crack']+=1
      if i['c_type']==2:
        if i['c_count_state']==0:
          seo_paidinfo['try']+=1
        elif i['c_count_state']==1:
          seo_paidinfo['normal']+=1
        elif i['c_count_state']==-1:
          seo_paidinfo['stop']+=1
        elif i['c_count_state']==-2:
          seo_paidinfo['crack']+=1
      if i['c_type']==1:
        if i['c_count_state']==0:
          sem_paidinfo['try']+=1
        elif i['c_count_state']==1:
          sem_paidinfo['normal']+=1
        elif i['c_count_state']==-1:
          sem_paidinfo['stop']+=1
        elif i['c_count_state']==-2:
          sem_paidinfo['crack']+=1
    
    sql="SELECT a.*,c.c_pay_time,c.c_pay_amount FROM  t_user_info a join t_finance_info c on a.c_user_id=c.c_user_id"
    print sql
    cursor.execute(sql)
    result=dictfetchall(cursor) 
    weibo_paidinfo_list=[]
    seo_paidinfo_list=[]
    sem_paidinfo_list=[]
    for i in result:
      if i['c_type']==0:
        weibo_paidinfo_list.append(i)
      if i['c_type']==2:
        seo_paidinfo_list.append(i)
      if i['c_type']==1:
        sem_paidinfo_list.append(i)

    template = loader.get_template('userinfo_paidinfo.html')
    params= Context({"weibo_paidinfo_list":weibo_paidinfo_list,"seo_paidinfo_list":seo_paidinfo_list,"sem_paidinfo_list":sem_paidinfo_list,"weibo_paidinfo":weibo_paidinfo,"seo_paidinfo":seo_paidinfo,"sem_paidinfo":sem_paidinfo,"username":username})
    return HttpResponse(template.render(params))



@login_required
def use_time(request):
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    
    cursor = connection.cursor()
    sql="SELECT a.date,a.online_time,a.c_user_id,b.c_user_name FROM user_online_time a LEFT JOIN t_user_info b ON a.c_user_id=b.c_user_id ORDER BY a.online_time DESC"
    print sql
    cursor.execute(sql)
    result_list=dictfetchall(cursor)

    after_range_num = 3
    befor_range_num = 4


    try:
      page = int(request.GET.get("page",1))
      if page < 1:
        page = 1
    except ValueError:
      page = 1
    paginator = Paginator(result_list,50)
    try:
      search_result = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
      search_result = paginator.page(paginator.num_pages)
    if page >= after_range_num:
      page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
    else:
      page_range = paginator.page_range[0:int(page)+befor_range_num]    


    template = loader.get_template('userinfo_use_time.html')
    params= Context({"result_list":search_result,"username":username,'page_range':page_range})
    return HttpResponse(template.render(params))


@login_required
def get_online_users(request):

    cursor = connection.cursor()
    sql="SELECT count(*) FROM t_user_info WHERE c_online_state =1 "
    cursor.execute(sql)
    result=cursor.fetchall() 
    params= {"result":result[0][0]}
    return HttpResponse(json.dumps(params))

@login_required
def online_users(request):
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
    sql="SELECT count(*) FROM  t_user_info "
    print sql
    cursor.execute(sql)
    total_users=cursor.fetchall() 

    sql="SELECT * FROM  t_user_info WHERE  c_online_state =1  "
    print sql
    cursor.execute(sql)
    online_share=dictfetchall(cursor) 


    weibo_online={"try":0,"normal":0,"stop":0,"crack":0}
    seo_online={"try":0,"normal":0,"stop":0,"crack":0}
    sem_online={"try":0,"normal":0,"stop":0,"crack":0}
    online_weibo_total=0
    online_seo_total=0
    online_sem_total=0
    weibo_table_list=[]
    seo_table_list=[]
    sem_table_list=[]

    for i in online_share:
      if i['c_type']==0:
        weibo_table_list.append(i)
        online_weibo_total+=1
        if i['c_count_state']==0:
          weibo_online['try']+=1
        elif i['c_count_state']==1:
          weibo_online['normal']+=1
        elif i['c_count_state']==-1:
          weibo_online['stop']+=1
        elif i['c_count_state']==-2:
          weibo_online['crack']+=1
      if i['c_type']==2:
        seo_table_list.append(i)      
        online_seo_total+=1
        if i['c_count_state']==0:
          seo_online['try']+=1
        elif i['c_count_state']==1:
          seo_online['normal']+=1
        elif i['c_count_state']==-1:
          seo_online['stop']+=1
        elif i['c_count_state']==-2:
          seo_online['crack']+=1
      if i['c_type']==1:
        sem_table_list.append(i)              
        online_sem_total+=1
        if i['c_count_state']==0:
          sem_online['try']+=1
        elif i['c_count_state']==1:
          sem_online['normal']+=1
        elif i['c_count_state']==-1:
          sem_online['stop']+=1
        elif i['c_count_state']==-2:
          sem_online['crack']+=1
    template = loader.get_template('userinfo_online_users.html')
    params= Context({"weibo_table_list":weibo_table_list,"seo_table_list":seo_table_list,"sem_table_list":sem_table_list,"online_weibo_total":online_weibo_total,"online_seo_total":online_seo_total,"online_sem_total":online_sem_total,"weibo_online":weibo_online,"seo_online":seo_online,"sem_online":sem_online,"username":username,"total_users":total_users[0][0]})
    return HttpResponse(template.render(params))



@login_required
def get_online_users(request):

    cursor = connection.cursor()
    sql="SELECT count(*) FROM t_user_info WHERE c_online_state =1 "
    cursor.execute(sql)
    result=cursor.fetchall() 
    params= {"result":result[0][0]}
    return HttpResponse(json.dumps(params))


@login_required
def user_location(request):
    cursor = connection.cursor()
    
    username=None
    if request.user.is_authenticated():
        username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  

    sql="select c_city,count(*) c from t_user_action_log group by c_city"
    cursor.execute(sql)
    result_list=dictfetchall(cursor)
    print result_list
    city_list=[]
    table_list=result_list
    for i in result_list:
      city_list.append([i['c_city'],i['c']])      


    city_list = json.dumps(city_list)
    result_list = json.dumps(result_list)

    after_range_num = 3
    befor_range_num = 4


    try:
      page = int(request.GET.get("page",1))
      if page < 1:
        page = 1
    except ValueError:
      page = 1
    paginator = Paginator(table_list,50)
    try:
      search_result = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
      search_result = paginator.page(paginator.num_pages)
    if page >= after_range_num:
      page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
    else:
      page_range = paginator.page_range[0:int(page)+befor_range_num]    



    template = loader.get_template('userinfo_user_location.html')
    params= Context({'page_range':page_range,"table_list":search_result,"result_list":result_list,"city_list":city_list,"username":username})
    return HttpResponse(template.render(params))



@login_required
def user_list(request):
    
    admin_username=None
    if request.user.is_authenticated():
        admin_username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    para_str='no=no' 
    allquery=1
    try:
      userid=int(request.GET['userid'])
    except:
      userid=None
    else:
      allquery=0
      para_str+='&userid=%s' % userid 
    try:
      username=request.GET['username']
    except:
      username=None
    else:
      allquery=0
      para_str+='&username=%s' % username

    try:
      realname=request.GET['realname']
    except:
      realname=None
    else:
      allquery=0
      para_str+='&realname=%s' % realname
    try:
      company=request.GET['company']
    except:
      company=None
    else:
      allquery=0
      para_str+='&company=%s' % company
    try:
      mail=request.GET['mail']
    except:
      mail=None
    else:
      allquery=0
      para_str+='&mail=%s' % mail
    try:
      tel=request.GET['tel']
    except:
      tel=None
    else:
      allquery=0
      para_str+='&tel=%s' % tel

    try:
      state_test=int(request.GET['state_test'])
    except:
      state_test=None
    else:
      allquery=0
      para_str+='&state_test=%s' % state_test

    try:
      state_normal=int(request.GET['state_normal'])
    except:
      state_normal=None
    else:
      allquery=0
      para_str+='&state_normal=%s' % state_normal
    try:
      state_stop=int(request.GET['state_stop'])
    except:
      state_stop=None
    else:
      allquery=0
      para_str+='&state_stop=%s' % state_stop
    try:
      state_crack=int(request.GET['state_crack'])
    except:
      state_crack=None
    else:
      allquery=0
      para_str+='&state_crack=%s' % state_crack
    try:
      type_weibo=int(request.GET['type_weibo'])
    except:
      type_weibo=None
    else:
      allquery=0
      para_str+='&type_weibo=%s' % type_weibo
    try:
      type_seo=int(request.GET['type_seo'])
    except:
      type_seo=None
    else:
      allquery=0
      para_str+='&type_seo=%s' % type_seo
    try:
      type_sem=int(request.GET['type_sem'])
    except:
      type_sem=None
    else:
      allquery=0
      para_str+='&type_sem=%s' % type_sem

    print "=====>>>>>",para_str 

    after_range_num = 3
    befor_range_num = 4

    cursor = connection.cursor()
    sql="SELECT * FROM t_user_info WHERE 1=1 "
    
    if userid and userid !='':
      sql+= " AND c_user_id=%s " %userid
    else: 
      userid=None
    if username and username !='':
      sql+= " AND c_user_name like %s " #%username
    else:
      username=None
    if realname and realname !='':
      sql+= " AND c_real_name like %s " # %realname
    else:
      realname=None
    
    if company and company !='':
      sql+= " AND c_company_name  like %s "  #%company
    else:
      company=None
    if mail and mail !='':
      sql+= " AND c_email_addr='%s' " %mail
    else:
      mail=None
    if tel and tel !='':
      sql+= " AND c_phone_no='%s' " %tel
    else:
      tel=None

    state_str=""
    if state_normal!=None:
      state_str+=str(state_normal)+","
    if state_stop!=None:
      state_str+=str(state_stop)+","
    if state_crack!=None:
      state_str+=str(state_crack)+","
    if state_test!=None:
      state_str+=str(state_test)+","
    state_str=state_str.rstrip(',')
    state_str="("+state_str+")"
    if state_normal!=None or  state_stop!=None or state_crack!=None or state_test!=None:
      sql+= " AND c_count_state in %s " %state_str
    

    type_str=""
    print type_weibo
    if type_weibo!=None:
      type_str+="0,"
    if type_seo!=None:
      type_str+="2,"
    if type_sem!=None:
      type_str+="1,"
    type_str=type_str.rstrip(',')
    type_str="("+type_str+")"
    if type_weibo!=None or type_seo!=None or type_sem!=None:
      sql+= " AND c_type in %s " %type_str
    
    
    print sql
    para_list=[]
    if username:
      para_list.append('%'+username+'%')
    if realname:
      para_list.append('%'+realname+'%')
    if company:
      para_list.append('%'+company+'%')

    cursor.execute(sql,para_list)
    result_list=dictfetchall(cursor)

    try:
      page = int(request.GET.get("page",1))
      if page < 1:
        page = 1
    except ValueError:
      page = 1
    paginator = Paginator(result_list,30)
    try:
      search_result = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
      search_result = paginator.page(paginator.num_pages)
    if page >= after_range_num:
      page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
    else:
      page_range = paginator.page_range[0:int(page)+befor_range_num]    


    template = loader.get_template('userinfo_user_list.html')
    params= Context({"cur_url":para_str,"result_list":search_result,"username":admin_username,'page_range':page_range})
    return HttpResponse(template.render(params))






@login_required
def payhistory(request):
    admin_username=None
    if request.user.is_authenticated():
        admin_username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    para_str='no=no' 
    allquery=1
    try:
      userid=int(request.GET['userid'])
    except:
      userid=None
    else:
      allquery=0
      para_str+='&userid=%s' % user_id
    try:
      username=request.GET['username']
    except:
      username=None
    else:
      allquery=0
      para_str+='&username=%s' % username

    try:
      realname=request.GET['realname']
    except:
      realname=None
    else:
      allquery=0
      para_str+='&realname=%s' % realname
    try:
      company=request.GET['company']
    except:
      company=None
    else:
      allquery=0
      para_str+='&company=%s' % company
    try:
      mail=request.GET['mail']
    except:
      mail=None
    else:
      allquery=0
      para_str+='&mail=%s' % mail
    try:
      tel=request.GET['tel']
    except:
      tel=None
    else:
      allquery=0
      para_str+='&tel=%s' % tel
    try:
      state_test=int(request.GET['state_test'])
    except:
      state_test=None
    else:
      allquery=0
      para_str+='&state_test=%s' % state_test
    try:
      state_normal=int(request.GET['state_normal'])
    except:
      state_normal=None
    else:
      allquery=0
      para_str+='&state_normal=%s' % state_normal
    try:
      state_stop=int(request.GET['state_stop'])
    except:
      state_stop=None
    else:
      allquery=0
      para_str+='&state_stop=%s' % state_stop

    try:
      state_crack=int(request.GET['state_crack'])
    except:
      state_crack=None
    else:
      allquery=0
      para_str+='&state_crack=%s' % state_crack

    try:
      type_weibo=int(request.GET['type_weibo'])
    except:
      type_weibo=None
    else:
      allquery=0
      para_str+='&type_weibo=%s' % type_weibo
    try:
      type_seo=int(request.GET['type_seo'])
    except:
      type_seo=None
    else:
      allquery=0
      para_str+='&type_seo=%s' % type_seo
    try:
      type_sem=int(request.GET['type_sem'])
    except:
      type_sem=None
    else:
      allquery=0
      para_str+='&type_sem=%s' % type_sem

    

    after_range_num = 3
    befor_range_num = 4

    cursor = connection.cursor()
    sql="SELECT t_user_info.*,a.c_pay_time,a.c_pay_amount FROM t_user_info  join t_finance_info a on t_user_info.c_user_id=a.c_user_id WHERE 1=1 "
    
    if userid and userid !='':
      sql+= " AND c_user_id=%s " %userid
    else: 
      userid=None
    if username and username !='':
      sql+= " AND c_user_name like %s " # %username
    else:
      username=None
    if realname and realname !='':
      sql+= " AND c_real_name like %s "# %realname
    else:
      realname=None
    
    if company and company !='':
      sql+= " AND c_company_name like %s "# %company
    else:
      company=None
    if mail and mail !='':
      sql+= " AND c_email_addr='%s' " %mail
    else:
      mail=None
    if tel and tel !='':
      sql+= " AND c_phone_no='%s' " %tel
    else:
      tel=None

    state_str=""
    if state_normal!=None:
      state_str+=str(state_normal)+","
    if state_stop!=None:
      state_str+=str(state_stop)+","
    if state_crack!=None:
      state_str+=str(state_crack)+","
    if state_test!=None:
      state_str+=str(state_test)+","
    state_str=state_str.rstrip(',')
    state_str="("+state_str+")"
    if state_normal!=None or  state_stop!=None or state_crack!=None or state_test!=None:
      sql+= " AND c_count_state in %s " %state_str
    

    type_str=""
    print type_weibo
    if type_weibo!=None:
      type_str+="0,"
    if type_seo!=None:
      type_str+="2,"
    if type_sem!=None:
      type_str+="1,"
    type_str=type_str.rstrip(',')
    type_str="("+type_str+")"
    if type_weibo!=None or type_seo!=None or type_sem!=None:
      sql+= " AND c_type in %s " %type_str
    
    print sql
    para_list=[]
    if username:
      para_list.append('%'+username+'%')
    if realname:
      para_list.append('%'+realname+'%')
    if company:
      para_list.append('%'+company+'%')
    
    print sql
    
    cursor.execute(sql,para_list)
    result_list=dictfetchall(cursor)

    try:
      page = int(request.GET.get("page",1))
      if page < 1:
        page = 1
    except ValueError:
      page = 1
    paginator = Paginator(result_list,30)
    try:
      search_result = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
      search_result = paginator.page(paginator.num_pages)
    if page >= after_range_num:
      page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
    else:
      page_range = paginator.page_range[0:int(page)+befor_range_num]    


    template = loader.get_template('userinfo_payhistory.html')
    params= Context({"cur_url":para_str,"result_list":search_result,"username":admin_username,'page_range':page_range})
    return HttpResponse(template.render(params))
