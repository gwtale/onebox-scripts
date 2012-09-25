# -*- coding:utf-8 -*-
# @ericyue
# hi.moonlight@gmail.com
import time
import sys
import os
import json

middle_result={}

def inc_counts(session):
  global middle_result
  if session['query'] not in middle_result:
    middle_result[session['query']]={'search':0,'page':0}
  
  if session['page']<0 and session['action']=='se':
    middle_result[session['query']]['search']+=1
  elif session['action']=='se' and session['page']>0:
    middle_result[session['query']]['page']+=1  

def merge(str1):
  
  global current_list #store whole sessions(between the empty line) 
  global current_session

  if len(str1.split('\t'))==2:
    current_list=[]
    current_session={}
  else:
    items=str1.split('\t')
    if len(items)!=13:
      return
    if items[4]!='onebox':
      return
    current_session['query']=items[2]
    current_session['action']=items[3]
    current_session['page']=int(items[6])
    current_list.append(current_session)
    
    inc_counts(current_session)
    current_session={}
if __name__=="__main__":
  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break

