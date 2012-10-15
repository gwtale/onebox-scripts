#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import os.path
import sys
import getopt
sys.path.append('/home/yuebin/onebox-scripts/findnewsquery/conf')
import config
from datetime import *

hadoop_streaming_file = "/home/yuebin/.hadoop/hadoop/contrib/streaming/hadoop-0.20.1.11-fb-streaming.jar"
hadoop_home_path = "~/.hadoop/hadoop/"

homepath = '/home/yuebin/onebox-scripts/findnewsquery/'
binpath = homepath + '/bin/'
confpath = homepath + '/conf/'
datapath = homepath+'/' 
logpath = homepath + '/log/'

MAPPER_FILE_NAME = ""
REDUCER_FILE_NAME = ""
LOG = False
INPUT_PATH=""


OUTPUT_PATH = ""

def alert(alert_content):
    alert_url="http://alarms.ops.qihoo.net:8360/intfs/sms_intf?"
    mobiles="18201379767"#|18618141031"
    alert_time=str(datetime.now())[:16]
    msg="[serving][findnewsquery][m03][%s]" %(alert_content)
    params={"mobiles":mobiles,"msg":msg.decode('utf8').encode('gbk')}
    postdata = urllib.urlencode(params)
    req=alert_url+postdata
    res = urllib2.urlopen(req).read()

if __name__ == "__main__":
  try:
    DEBUG_DAY=int(sys.argv[1])
  except:
    DEBUG_DAY=1
  print "DELAY",DEBUG_DAY
  today = str(datetime.now()-timedelta(DEBUG_DAY)).split(' ')[0]
  hadoop_timeout = 600
  print 'start day:',today
    
  end = datetime.now()-timedelta(DEBUG_DAY)
  for i in range(0,9):
    tmp_date=end-timedelta(i)
    TMP_P=" /user/hehaitao/clickmodel/"+str(tmp_date).split(' ')[0].replace('-','')+"/querylog.st/ "
    if config.has_hadoop_dir(TMP_P):
      INPUT_PATH+=TMP_P
  OUTPUT_PATH='/user/yuebin/hadoop/findnewsquery/%s.st' %(today.replace('-',''))
  print "INPUT PATH:",INPUT_PATH
  print "OUTPUT PATH",OUTPUT_PATH
  ret = 0
  command =  hadoop_home_path+"/bin/hadoop jar " + hadoop_streaming_file + \
          " -input " + INPUT_PATH +\
          " -output  "+ OUTPUT_PATH + \
          " -mapper \" python findnewsquery_mapper.py \"  " + \
          " -reducer \" python findnewsquery_reducer.py "+ str(DEBUG_DAY)+" \" " +\
          " -file " + binpath +"findnewsquery_mapper.py " + \
          " -file " + binpath + "findnewsquery_reducer.py " + \
          " -file " + confpath + "config.py"  + \
          " -jobconf mapred.reduce.tasks=12 " + \
          " -jobconf mapred.job.name=\"find_news_query_"+today+"\" "  +\
          " -jobconf mapred.job.priority=NORMAL" +\
          " -cacheArchive '/user/yuebin/suffixtree.tar.gz#suffixtree' "
  print command
  ret = config.run_hadoop_retry(command,OUTPUT_PATH)
  if ret!=0:
    alert("findnewsquery job faild")
