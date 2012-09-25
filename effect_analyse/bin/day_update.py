#coding=utf-8
import sys
import os
import urllib2
import urllib
from datetime import *

def alert(alert_content):
    alert_url="http://alarms.ops.qihoo.net:8360/intfs/sms_intf?"
    mobiles="18201379767"#|18618141031"
    alert_time=str(datetime.now())[:16]
    msg="[serving][day_effect_update][m03][%s]" %(alert_content)
    params={"mobiles":mobiles,"msg":msg.decode('utf8').encode('gbk')}
    postdata = urllib.urlencode(params)
    req=alert_url+postdata
    res = urllib2.urlopen(req).read()

ENGINE=["baidu","google","qss","onebox","other"]
URL="http://127.0.0.1:8889/external?"

def build_url(cur_time,items):
  urls=[]
  global ENGINE
  global URL
  print items
  pos=0
  for i in items[1:]:
    c_timestamp=cur_time
    params={"key":items[0],"value":i,"timestamp":c_timestamp,"freq":'day',"action":'update',"engine":ENGINE[pos]}
    postdata = urllib.urlencode(params)
    req = URL+postdata
    urls.append(req)
    pos+=1
  return urls

if __name__=="__main__":
  try:
    DEBUG_DAY=int(sys.argv[1])
  except:
    DEBUG_DAY=1
  date=str(datetime.now()-timedelta(DEBUG_DAY)).split(' ')[0].replace('-','')
  remote="/user/yuebin/hadoop/effect_analyse/%s.st" %date
  local="/home/yuebin/effect_analyse/data/%s.st" %date
  os.system("rm -rf "+local)
  copy="~/.hadoop/hadoop/bin/hadoop fs -copyToLocal %s %s" %(remote,local)
  print copy
  os.system(copy)
  content=open(local+'/part-00000').readlines()
  #cur_time=str(datetime.now()-timedelta(DEBUG_DAY))
  print content
  cur_time=content[0]
  print "cur_time",cur_time
  for line in content[1:]:
    items=line.rstrip('\n').split('\t')
    urls=build_url(cur_time,items)
    for u in urls:
        print u
        res = urllib2.urlopen(u).read()
        if res!="ok":
          print res
          alert("faild")
        
