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

def merge(str1):
  global sessions
  str1=str1.rstrip("\n")
  items = str1.split("\t")

  if items[0] in sessions:
    if items[1] in sessions[items[0]]:
      sessions[items[0]][items[1]]+=1
    else:
      sessions[items[0]][items[1]]=1
  else:
    sessions[items[0]]={}
    sessions[items[0]][items[1]]=1

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
    for i in sessions:
      if s==i:
        continue
      click_same=same_items_num(sessions[s],sessions[i])
      if click_same!=0:
        marks[i]=click_same
    if len(marks)!=0:
      marks=sorted(marks.iteritems(),key=lambda x:(-x[1]))
      print s
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

#  for s in sessions:
#    if len(sessions[s])<5:
#      continue
#    limit=0
#    tmp=sorted(sessions[s].iteritems(),key=lambda x:(-x[1]))
#    print s
#    for i in tmp:
#      limit+=1
#      if limit>50:
#        break
#      print i[0],i[1]
#    print "="*40
