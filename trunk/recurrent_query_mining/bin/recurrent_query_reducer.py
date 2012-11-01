#!/usr/bin/python
# -*- coding:utf-8 -*-

# 
# find news query
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

DELAY=1
#save all processed items
query={}

def alert(alert_content):
  alert_url="http://alarms.ops.qihoo.net:8360/intfs/sms_intf?"
  mobiles="18201379767"#|18618141031"
  alert_time=str(datetime.now())[:16]
  msg="[serving][findnewsquery][m03][%s][%s]" %(alert_time,alert_content)
  params={"mobiles":mobiles,"msg":msg.decode('utf8').encode('gbk')}
  postdata = urllib.urlencode(params)
  req=alert_url+postdata
  res = urllib2.urlopen(req).read()
  if res.strip()!='ok':
    raise Exception(req,res)

def merge(str1):
  global query

  str1=str1.rstrip("\n")
  items = str1.split("\t")
  keyword = items[0]
  #debug
  if keyword not in query:
    query[keywords]={'date':items[1],'counts':1}
  else:
    query[keywords]['counts']+=1

def sortdict(adict):
  return sorted(result.iteritems(), key=lambda x:(-x[1]['date']))

if __name__=='__main__':
    global DELAY
    try:
      DELAY=int(sys.argv[1])
    except:
      DELAY=1
    while True :
      try:
        line = raw_input()
        merge(line)
      except EOFError:
        break
    
    inc_marks=sortdict(query)
    for i in inc_marks:
      print "%s\t%s\t%s\t%s\t%s" % (i[0],i[1]['date'],i[1]['counts'])
    
  

