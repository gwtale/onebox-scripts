# -*- coding:utf-8 -*-

#
# find news query 
# @ericyue
#

import time
import sys
import os
from datetime import datetime
import urllib
import urllib2
import re

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

regx=r"[0-9]{11}|www|com|net|cn|org|http|成人|av|\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
skip=re.compile(regx)

all_nums=r"[0-9]{8}|[0-9]{4}"
all_nums_regx=re.compile(all_nums)

try:
  path=os.environ['map_input_file']
  date=path.split("clickmodel/")[1].split("/querylog.st")[0][4:]
except:
  date='0711'

while True :
  try:
    line = raw_input().rstrip('\n');
    items = line.split( '\t' )
    word = items[0].strip()
    if word.find('大乐透')!==-1 :#and all_nums_regx.match(word):
      continue
    if word!='':
      search_counts = 0.5*float(items[1])+1.85*float(items[2])
      print "%s\t%s\t%s" % ( word,date,int(search_counts)+1)
  except EOFError:
    break
