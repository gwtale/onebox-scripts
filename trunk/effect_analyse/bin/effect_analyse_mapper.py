# -*- coding:utf-8 -*-

# effect analysenalyse
# @ericyue
# hi.moonlight@gmail.com
import time
import sys
import os
import json


def init_vars():
  return {"baidu":0.0,"google":0.0,"qss":0.0,"onebox":0.0,"other":0.0}

#第1-3位点击率
top3_click_counts=init_vars()
pos1_click_counts=init_vars()
pos2_click_counts=init_vars()
pos3_click_counts=init_vars()

#换query搜索比例
query_change_counts=init_vars()

#首次点击时间间隔
first_click_time=init_vars()
time_range_counts=init_vars()

#总的搜索次数,不含翻页
total_search_counts=init_vars()
#总的点击统计
total_click_counts=init_vars()

#总的翻页次数统计
total_page_change_counts=init_vars()
#有翻页的搜索次数统计
total_page_change_insearch_counts=init_vars()

#无点击总数
total_non_click_counts=init_vars()

#临时变量
current_session={}
current_list=[]

#总的goal数目
total_goals=init_vars()

def inc_total_search_counts(session):
  global total_search_counts
  if session['page']<0 and session['action']=='se':
    total_search_counts[session['engine']]+=1 

def inc_total_click_counts(session):
  global total_click_counts
  if session['action']=='ck':
    total_click_counts[session['engine']]+=1 

def inc_top_click_counts(session):
  global top3_click_counts
  global pos1_click_counts
  global pos2_click_counts
  global pos3_click_counts
  
  if session['action']=='ck':
    if 'pos' in session['other_para']:
      try:
        pos=int(session['other_para']['pos'])
      except:
        return
      if pos<=3:
        if pos==1:
           pos1_click_counts[session['engine']]+=1 
        elif pos==2:
           pos2_click_counts[session['engine']]+=1 
        elif pos==3:
           pos3_click_counts[session['engine']]+=1 
        top3_click_counts[session['engine']]+=1 

def inc_total_page_change_counts(session):
  global total_page_change_counts
  if session['action']=='se' and session['page']>0:
    total_page_change_counts[session['engine']]+=1 


tmp_cur_se_query=None
page_insearch_flag=True

def inc_total_page_change_insearch_counts(session):
  global total_page_change_insearch_counts
  global current_session
  global tmp_cur_se_query
  global page_insearch_flag

  if session['action']!='se':
    return
  if session['query']!=tmp_cur_se_query:
    tmp_cur_se_query= session['query']
    page_insearch_flag=True
    return
  elif page_insearch_flag==False:
    return
  elif session['page']>0:
    total_page_change_insearch_counts[session['engine']]+=1
    page_insearch_flag=False

def devide_search_action(goal):
  search_list=[[]]
  if goal==[]:
    return None
  search_list[0].append(goal[0])
  for i in goal[1:]:
    if i['query']==search_list[-1][0]['query']:
      search_list[-1].append(i)
    else:
      search_list.append([])
      search_list[-1].append(i)
  return search_list
  

def divide_goal():
  global current_list
  goal_list=[[]]
  if current_list==[]:
    return None
  goal_list[0].append(current_list[0])
  for i in current_list[1:]:
    if i['goal_id']==goal_list[-1][0]['goal_id']:
      goal_list[-1].append(i)
    else:
      goal_list.append([])
      goal_list[-1].append(i)
  return goal_list


def non_click_search_counts(search_list):
  global total_non_click_counts
  for s in search_list:
    ck=0
    engine=None
    for j in s:
      engine=j['engine']
      if j['action']=='ck':
        ck=1
        break
    if ck==0:
      total_non_click_counts[engine]+=1

def first_click_time_counts(search_list):
  global first_click_time
  global time_range_counts
  for s in search_list:
    for j in s:
      if j['action']=='ck':
        time_range=j['timestamp']-s[s.index(j)-1]['timestamp']
        if time_range>0 and time_range<300:
          time_range_counts[j['engine']]+=1
          #print  j['timestamp'],'-',s[s.index(j)-1]['timestamp'],time_range
          first_click_time[j['engine']]+=time_range
          break

def analyse():
  global current_list
  global total_goals
  global query_change_counts

  goal_list=divide_goal()
  if goal_list==None:
    return 
  for i in goal_list:
    search_list=devide_search_action(i)
    first_click_time_counts(search_list)
    non_click_search_counts(search_list)
    query_set=set()
    engine=None
    for j in i:
      engine=j['engine']
      query_set.add(j['query'])
    len_set=len(query_set)
    total_goals[engine]+=1
    if len_set-1!=0:
      query_change_counts[engine]+=(len_set-1)
    
    
def merge(str1):
  
  global current_list #store whole sessions(between the empty line) 
  global current_session
  global tmp_cur_se_query

  if len(str1.split('\t'))==2:
    analyse()
    current_list=[]
    current_session={}
  else:
    items=str1.split('\t')
    if len(items)!=13:
      return
    current_session['session_id']=items[0]    
    current_session['date']=items[1]
    current_session['query']=items[2]
    current_session['action']=items[3]
    current_session['engine']=items[4]
    current_session['clickurl']=items[5]
    current_session['page']=int(items[6])
    current_session['other_para']=eval(items[7])
    current_session['next_action']=eval(items[8])
    current_session['goal_id']=items[9]
    current_session['click_weighing']=items[10]
    current_session['timestamp']=int(items[11])
    current_session['action_num']=items[12]
    current_list.append(current_session)
    
    inc_total_search_counts(current_session)
    inc_total_click_counts(current_session)
    inc_top_click_counts(current_session)

    inc_total_page_change_counts(current_session)
    inc_total_page_change_insearch_counts(current_session)

    current_session={}

def output(name,odict):
  baidu=odict['baidu']
  google=odict['google']
  qss=odict['qss']
  onebox=odict['onebox']
  other=odict['other']
  print "%s\t%s\t%s\t%s\t%s\t%s" %(name,baidu,google,qss,onebox,other)
  
if __name__=="__main__":
  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break

  output("total_click",total_click_counts)
  output("total_search",total_search_counts)

  output("time_range_counts",time_range_counts)
  output("first_click_time",first_click_time)

  output("non_click_counts",total_non_click_counts)

  output("top3_click_counts",top3_click_counts)
  output("pos1_click_counts",pos1_click_counts)
  output("pos2_click_counts",pos2_click_counts)
  output("pos3_click_counts",pos3_click_counts)

  output("query_change_counts",query_change_counts)
  output("page_change_counts",total_page_change_counts)
  output("page_change_insearch_counts",total_page_change_insearch_counts)
  output("total_goals",total_goals)


