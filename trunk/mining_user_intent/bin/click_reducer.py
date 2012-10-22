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
    try:
      query_click=int(query.split('#')[1])
      query_search=int(query.split('#')[2])
    except:
      raise Exception(query)
    if query_str not in result:
      result[query_str]={"click":query_click,"user":1,"search":query_search}
    else:
      result[query_str]["click"]+=query_click
      result[query_str]["search"]+=query_search
      result[query_str]['user']+=1

  return sorted(result.iteritems(), key=lambda x:(-x[1]['user'],-x[1]['click'],-x[1]['search']))

def output_session(session):
  global first_item_count
  global whole_sessions
  if first_item_count==1:
    return
  whole_sessions.append({"session":session,"counts":first_item_count})

def fscore(m1,m2):
  return m1/float(m2)

def merge(str1):
  global current_session
  global first_item_count
  str1=str1.rstrip("\n")
  items = str1.split("\t")
  query = Query()
  query.query= items[0]
  query.click= float(items[1].split('#')[0])
  query.search= float(items[1].split('#')[1])
  if query.query !=current_session.items()[0][0]:
    output_session(current_session)
    current_session={}
    first_item_count=1
    current_session[query.query]=[]
    current_session[query.query]+=items[2:]
  else:
    current_session[query.query]+=items[2:]
    first_item_count+=1

if __name__=='__main__':

  line = raw_input()
  cur_line=line.rstrip("\n")
  items = cur_line.split("\t")
  query_str=items[0]
  current_session[query_str]=[]
  current_session[query_str]+=items[2:]
  first_item_count=1
  while True:
    try:
      line = raw_input()
      merge(line)
    except EOFError:
      break
  whole_sessions.sort(cmp=lambda x,y: cmp(x['counts'],y['counts']),reverse=True)
  for i in whole_sessions:
    processed=i['session'].items()[0][1]
    p_order=sort_list(processed)
    flag=True
    counter=0
    for pi in p_order:
      if len(pi[0])<len(i['session'].items()[0][0])*0.8:
        continue
      elif pi[1]['user']<3 or pi[1]['click']<5:
        continue
      else:
        if flag:
          print i['session'].items()[0][0],i['counts']
          flag=False
        print "===>",pi[0],pi[1]['user'],pi[1]['click'],pi[1]['search'],fscore(pi[1]['click'],pi[1]['search'])
        counter+=1
      if counter>40:
        break
    if flag==False:
      print "---"*20

