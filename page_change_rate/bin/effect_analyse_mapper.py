# -*- coding:utf-8 -*-
# @ericyue
# hi.moonlight@gmail.com
import time
import sys
import os
import json

def inc_total_search_counts(session):
  global total_search_counts
  if session['page']<0 and session['action']=='se':
    total_search_counts[session['engine']]+=1 
def inc_total_page_change_counts(session):
  global total_page_change_counts
  if session['action']=='se' and session['page']>0:
    total_page_change_counts[session['engine']]+=1 

 
def analyse():
  global current_list
  global total_goals
  global query_change_rate


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
      query_change_rate[engine]+=(len_set-1)
    
    
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
    inc_first_to_third_click_rate(current_session)
    inc_total_page_change_counts(current_session)
    inc_total_page_change_insearch_counts(current_session)

    current_session={}
def calc_page_change_rate():
  global total_page_change_counts
  global total_page_change_insearch_counts

  try:
    baidu=total_page_change_counts['baidu']/total_search_counts['baidu']
  except:
    baidu=0.0
  try:
    google=total_page_change_counts['google']/total_search_counts['google']
  except:
    google=0.0
  try:
    onebox=total_page_change_counts['onebox']/total_search_counts['onebox']
  except:
    onebox=0.0
  try:
    qss=total_page_change_counts['qss']/total_search_counts['qss']
  except:
    qss=0.0
  try:
    other=total_page_change_counts['other']/total_search_counts['other']
  except:
    other=0.0

  print "page_change_rate\t%s\t%s\t%s\t%s\t%s" %(baidu,google,qss,onebox,other)
if __name__=="__main__":
  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break

  calc_click_rate()
  calc_first_to_third_click_rate()
  calc_page_change_rate()
  calc_query_change_rate()
  calc_non_click_rate()
  calc_first_click_time()
  output_total_search()
  output_total_click()

