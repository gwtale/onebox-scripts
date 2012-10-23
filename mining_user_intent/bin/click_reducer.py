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
import base64
import re
from datetime import datetime,timedelta
from operator import itemgetter

sessions={}
processed=set()
def merge(str1):
  global sessions
  str1=str1.rstrip("\n")
  items = str1.split("\t")

  if items[0] in sessions:
    sessions[items[0]]['counts']+=1
    if items[1] in sessions[items[0]]['all']:
      sessions[items[0]]['all'][items[1]]+=1
    else:
      sessions[items[0]]['all'][items[1]]=1
  else:
    sessions[items[0]]={'all':{},'counts':1}
    sessions[items[0]]['all'][items[1]]=1

def same_items_num(dict1,dict2): 
  total=0
  for i in dict1:
    if i in dict2:
      total+=1
  return total

def process():
  global sessions
  for s in sessions:
    marks={}
    if s in processed:
      continue
    for i in sessions:
      if s==i or i in processed:
        continue
      click_same=same_items_num(sessions[s]['all'],sessions[i]['all'])
      if click_same!=0:
        marks[i]=click_same
        processed.add(i)
    if len(marks)!=0:
      marks=sorted(marks.iteritems(),key=lambda x:(-x[1]))
      print s,sessions[s]['counts']
      for i in marks:
        print i[0],i[1]
      print "="*70
    
if __name__=='__main__':

  while True:
    try:
      line = raw_input()
      merge(line)
    except EOFError:
      break
  process()
