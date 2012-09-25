#!/usr/bin/python
# -*- coding:utf-8 -*-
import multiprocessing
import time as otime
import urllib
import os
import urllib2
import os.path
import sys
import getopt
sys.path.append('/home/yuebin/findnewsquery/conf')
import config
from datetime import *
import logging
LEVELS={'debug':logging.DEBUG,
                'info':logging.INFO,
                'warning':logging.WARNING,
                'error':logging.ERROR,
                'critical':logging.CRITICAL}
level_name = "debug" #defalut

hadoop_streaming_file = "/home/yuebin/.hadoop/hadoop/contrib/streaming/hadoop-0.20.1.11-fb-streaming.jar"
hadoop_home_path = "~/.hadoop/hadoop/"

homepath = '/home/yuebin/findnewsquery/'
binpath = homepath + '/bin/'
confpath = homepath + '/conf/'
datapath = homepath+'/' 
logpath = homepath + '/log/'

MAPPER_FILE_NAME = ""
REDUCER_FILE_NAME = ""
LOG = False

def alert(alert_content):
    alert_url="http://alarms.ops.qihoo.net:8360/intfs/sms_intf?"
    mobiles="18201379767"#|18618141031"
    alert_time=str(datetime.now())[:16]
    msg="[serving][findnewsquery][m03][%s]" %(alert_content)
    params={"mobiles":mobiles,"msg":msg.decode('utf8').encode('gbk')}
    postdata = urllib.urlencode(params)
    req=alert_url+postdata
    res = urllib2.urlopen(req).read()

def one_day(DEBUG_DAY):  
  #get_option()
    INPUT_PATH=""
    OUTPUT_PATH=""
    today = str(datetime.now()-timedelta(DEBUG_DAY)).split(' ')[0]
    hadoop_timeout = 600
    print 'start day:',today
    
    end = datetime.now()-timedelta(DEBUG_DAY)
    for i in range(1,6):
      tmp_date=end-timedelta(i)
      INPUT_PATH+= " /user/hehaitao/clickmodel/"+str(tmp_date).split(' ')[0].replace('-','')+"/querylog.st/ "
    OUTPUT_PATH='/user/yuebin/hadoop/findnewsquery/%s.st' %(today.replace('-',''))
    print "INPUT PATH:",INPUT_PATH
    print "OUTPUT PATH",OUTPUT_PATH
    ret = 0
    command =  hadoop_home_path+"/bin/hadoop jar " + hadoop_streaming_file + \
          " -input " + INPUT_PATH +\
          " -output  "+ OUTPUT_PATH + \
          " -mapper \" python findnewsquery_mapper.py \"  " + \
          " -reducer \" python findnewsquery_reducer.py \" " +\
          " -file " + binpath +"findnewsquery_mapper.py " + \
          " -file " + binpath + "findnewsquery_reducer.py " + \
          " -file " + confpath + "config.py"  + \
          " -jobconf mapred.reduce.tasks=4 " + \
          " -jobconf mapred.job.name=\"find_news_query_+"+today+"\" "  +\
          " -jobconf mapred.job.priority=NORMAL" +\
          " -cacheArchive 'hdfs://n01.dong.shgt.qihoo.net:9000/user/yuebin/suffixtree.tar.gz#suffixtree' "
    print command
    ret = config.run_hadoop_retry(command,OUTPUT_PATH)
    if ret!=0:
      alert("findnewsquery job faild")


if __name__ == "__main__":
  for i in range(5):
    th=multiprocessing.Process(target=one_day, args=(i,))
    th.start()
    otime.sleep(5)
    print "add.."
