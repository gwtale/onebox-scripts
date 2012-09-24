#!/usr/bin/python
# -*- coding:utf-8 -*-

# 
# mining user intent 
# @ericyue
#

import sys
import time
import math
import urllib
import urllib2
import base64
import re
from datetime import datetime,timedelta
from operator import itemgetter

current_session={}
first_item_count=0
whole_sessions=[]
def sort_list(llist):
  result={}
  for i in llist:
    i=str(i)
    if i not in result:
      result[i]=1
    else:
      result[i]+=1
  return sorted(result.iteritems(), key=itemgetter(1), reverse=True)

def output_session(session):
  global first_item_count
  global whole_sessions
  if first_item_count==1:
    return
  whole_sessions.append({"session":session,"counts":first_item_count})
  #print session.items()[0][0],first_item_count
  #processed=session.items()[0][1]
  #p_order=sort_list(processed)
  #for i in p_order:
  #  print "===>",i[0],i[1]
  #print "---"*20
def merge(str1):
  global current_session
  global first_item_count
  str1=str1.rstrip("\n")
  items = str1.split("\t")
  query = items[0]
  if query !=current_session.items()[0][0]:
    #print current_session
    #print ".........."
    output_session(current_session)
    current_session={}
    first_item_count=1
    current_session[items[0]]=[]
    current_session[items[0]]+=items[1:]
  else:
    current_session[items[0]]+=items[1:]
    first_item_count+=1
if __name__=='__main__':

  line = raw_input()
  cur_line=line.rstrip("\n")
  items = cur_line.split("\t")
  current_session[items[0]]=[]
  current_session[items[0]]+=items[1:]
  first_item_count=1
  while True :
    try:
      line = raw_input()
      merge(line)
    except EOFError:
      break
  whole_sessions.sort(cmp=lambda x,y: cmp(x['counts'],y['counts']),reverse=True)
  for i in whole_sessions:
    print i['session'].items()[0][0],i['counts']
    processed=i['session'].items()[0][1]
    p_order=sort_list(processed)
    for pi in p_order:
      print "===>",pi[0],pi[1]
    print "---"*20
   
