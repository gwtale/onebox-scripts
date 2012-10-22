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

if __name__=='__main__':

  while True:
    try:
      line = raw_input()
      merge(line)
    except EOFError:
      break
  for s in sessions:
    if len(sessions[s])<5:
      continue
    limit=0
    for i in sorted(sessions[s],reverse=True):
      limit+=1
      if limit>50:
        break
      print i,sessions[s][i]
    print "="*40
