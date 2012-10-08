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

class Query:
  def __init__(self):
    self.query=''
    self.click=0
    self.search=0
def sort_list(llist):
  result={}
  for query in llist:
    query_str=query.split('#')[0]
    query_click=int(query.split('#')[1])
    query_search=int(query.split('#')[2])
    if query_str not in result:
      result[query_str]={"click":query_click,"user":1,"search":query_search}
    else:
      result[query_str]["click"]+=query_click
      result[query_str]['user']+=1

  return sorted(result.iteritems(), key=lambda x:(-x[1]['user'],-x[1]['click'],-x[1]['search']))
  #return sorted(result.iteritems(), key=lambda x:-fscore(0.2*x[1]['user'],0.8*x[1]['click']))
def output_session(session):
  global first_item_count
  global whole_sessions
  if first_item_count==1:
    return
  whole_sessions.append({"session":session,"counts":first_item_count})

def fscore(m1,m2):
  return 2*m1*m1/float((m1+m2))

def merge(str1):
  global current_session
  global first_item_count
  str1=str1.rstrip("\n")
  items = str1.split("\t")
  query = Query()
  query.query= items[0].split('#')[0]
  query.click= float(items[0].split('#')[1])
  query.search= float(items[0].split('#')[2])
  if query.query !=current_session.items()[0][0]:
    output_session(current_session)
    current_session={}
    first_item_count=1
    current_session[query.query]=[]
    current_session[query.query]+=items[1:]
  else:
    current_session[query.query]+=items[1:]
    first_item_count+=1

if __name__=='__main__':


  line = raw_input()
  cur_line=line.rstrip("\n")
  items = cur_line.split("\t")
  query_str=items[0].split('#')[0]
  current_session[query_str]=[]
  current_session[query_str]+=items[1:]
  first_item_count=1
  while True:
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
      if pi[1]['user']<2 or pi[1]['click']<2:
        continue
      else:
        print "===>",pi[0],pi[1]['user'],pi[1]['click'],pi[1]['search']
    print "---"*20

