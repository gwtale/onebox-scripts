#coding=utf-8
from django.http import HttpResponse
import re
from django.db import connection, transaction
from django.template import Context,loader
from tools.util import *
from datetime import *
import json
#support chinese
import sys
sys.path.append("~/effect_analyse_system/redis")
import redis
reload(sys)
sys.setdefaultencoding('utf-8')

ENGINE=("baidu","google","onebox","qss","other")

def index (request):
    now = datetime.now()
    cursor = connection.cursor()
    try:
        key=request.GET['key']
    except:
        key=None  
    try:
        value=float(request.GET['value'])
    except:
        value=None
    try:
        timestamp=request.GET['timestamp']
    except:
        timestamp=None
    try:
        freq=request.GET['freq']
    except:
        freq=None
    try:
        action=request.GET['action']
    except:
        action=None
    try:
        engine=request.GET['engine']
        if engine not in ENGINE:
          engine=None
    except:
        engine=None

    if key==None or value==None or timestamp==None or freq==None or action==None or engine==None:
      return HttpResponse("error,wrong parameters")
    
    sql="INSERT IGNORE INTO `keys` (`key_name`) values('%s')" %(key)
    print sql
    cursor.execute(sql)
    transaction.commit_unless_managed()
    
    sql="SELECT id FROM `keys` WHERE key_name='%s'" % (key)
    print sql
    cursor.execute(sql)
    transaction.commit_unless_managed()
    
    key_id=cursor.fetchall()[0][0]
    if action =="add":
      if freq=="day":
        timestamp=timestamp.split(' ')[0]        
        sql="INSERT INTO `item_day_values` (`key_id`,`timestamp`,`value`,`engine`) values(%s,'%s',%s,'%s') ON DUPLICATE KEY UPDATE value=value+%s" % (key_id,timestamp,value,engine,value)
      elif freq=="hour":
        #0000-00-00 00:00:00
        timestamp=timestamp[:14]+'00:00'      
        sql="INSERT INTO `item_hour_values` (`key_id`,`timestamp`,`value`,`engine`) values(%s,'%s',%s,'%s') ON DUPLICATE KEY UPDATE value=value+%s" % (key_id,timestamp,value,engine,value)
      elif freq=="minute":
        timestamp=timestamp[:17]+'00'              
        sql="INSERT INTO `item_minute_values` (`key_id`,`timestamp`,`value`,`engine`) values(%s,'%s',%s,'%s') ON DUPLICATE KEY UPDATE value=value+%s" % (key_id,timestamp,value,engine,value)
      else:
        return HttpResponse("error,wrong freq")
      print sql
    elif action=="update":
      if freq=="day":
        timestamp=timestamp.split(' ')[0]
        sql="INSERT INTO `item_day_values` (`key_id`,`timestamp`,`value`,`engine`) values(%s,'%s',%s,'%s') ON DUPLICATE KEY UPDATE value=%s" % (key_id,timestamp,value,engine,value)
      elif freq=="hour":
        timestamp=timestamp[:14]+'00:00'            
        sql="INSERT INTO `item_hour_values` (`key_id`,`timestamp`,`value`,`engine`) values(%s,'%s',%s,'%s') ON DUPLICATE KEY UPDATE value=%s" % (key_id,timestamp,value,engine,value)
      elif freq=="minute":
        timestamp=timestamp[:17]+'00'                      
        sql="INSERT INTO `item_minute_values` (`key_id`,`timestamp`,`value`,`engine`) values(%s,'%s',%s,'%s') ON DUPLICATE KEY UPDATE value=%s" % (key_id,timestamp,value,engine,value)
      else:
        return HttpResponse("error,wrong freq")
      print sql
    else:
      return HttpResponse("error,wrong action")
    
    cursor.execute(sql)
    transaction.commit_unless_managed()
    if cursor.rowcount==0:
      connection.close()
      return HttpResponse("error")
    else:
      connection.close()
      return HttpResponse("ok")

