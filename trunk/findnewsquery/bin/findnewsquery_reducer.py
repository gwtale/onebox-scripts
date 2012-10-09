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
DEBUG=False
#suffix tree support (using c extension)
if DEBUG==False:
  sys.path.append("./suffixtree")
  #import SuffixTree
  #found_result_tree=SuffixTree.SuffixTree()
  #tree_node_num=0
#temp vars
counts = []
current_word=''
found_result_tree={}
#ouput dicts
inc_marks={}
reverse_marks={}
DELAY=1
#save all processed items
pre_reverse_query={}
result_mark_len={}

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

def has_some_day(counts,cur_date):
  for i in counts:
    if i.find(cur_date)!=-1:
      return True
  return False

def merge(str1):
  global current_word
  global counts
  global pre_reverse_query
  global today_click_counts

  str1=str1.rstrip("\n")
  items = str1.split("\t")
  keyword = items[0]
  #debug
  if keyword !=current_word:
    end = datetime.now()
    cur_date_str=str(end-timedelta(DELAY)).split(' ')[0][5:].replace('-','')
  
    if len(counts)>=2 and has_some_day(counts,cur_date_str) and average(convert_counts(counts))>5:
      counts.sort()
      converterd_counts=convert_counts(counts)
      if calc_increase_rate(current_word,converterd_counts):
        pass
      else:
        pre_reverse_query[current_word]=converterd_counts
    counts = []
    counts.append("\t".join(items[1:]))
    current_word = keyword
  else:
    counts.append("\t".join(items[1:]))


def reverse_v2():
  for i in pre_reverse_query:
    flag=False
    for inc in inc_marks:
      if i.find(inc)!=-1:
        reverse_marks[i]=[inc_marks[inc][0]*0.8,pre_reverse_query[i]]
        flag=True
        break

def convert_counts(count):
  tmp=[]
  for i in count:
    tmp.append(float(i.split('\t')[1]))
  return tmp

def calc_increase_rate(word,data):
  inc_rate_tmp=[]
  query_counts=data
  sum_counts=sum(query_counts)
  if DEBUG:
    print "word:%s average counts:%s " %(word,average(query_counts))
  if average(query_counts)<14:
    if DEBUG:
      print "average too low,break"
    return False 
  cv=calc_CV(query_counts)
  if DEBUG:
    print "CV:",cv
  if cv<0.331:
    if DEBUG:
      print "CV too low,break!"
    return False
  for i in range(len(data)):
    query_counts_before=float(data[i])
    if query_counts_before==0.0:
      query_counts_before=1
    if i<len(data)-1:
      query_counts_last=float(data[i+1])
    else:
      break
    if query_counts_last>query_counts_before:
      base_rate=((query_counts_last-query_counts_before)/query_counts_before)
    else:
      base_rate=((query_counts_last-query_counts_before)/query_counts_last)
    rate=(math.log10(sum_counts))*(math.log10(sum_counts)/20)*base_rate
    if DEBUG:
      print "orginal rate:",rate
    if rate < 0.0:
      if i < len(data)-2:
        if DEBUG:
          print "increase -,not in two days"
        inc_rate_tmp.append((-1.0/math.pow((len(data)-i),2))*abs(rate))
      else:
        if DEBUG:
          print "increase -,in two days"
        inc_rate_tmp.append((-1)*math.pow(1.15,(i+1))*abs(rate))
    else:
      if i < len(data)-2:
        if DEBUG:
          print "increase +,not in two days"
        inc_rate_tmp.append((1.0/math.pow((len(data)-i),2.75))*rate)
      else:
        if DEBUG:
          print "increase +,in two days"
        if len(data)>2:
          max_before=max(data[:len(data)-2])
          fake_rate=(query_counts_last-max_before)/max_before
        else:
          fake_rate=2
        if DEBUG:
          print "fake rate:",fake_rate
        if fake_rate<0.0 or abs(fake_rate)<1.5:
          if DEBUG:
            print "fake increase,downgrade the marks"
          inc_rate_tmp.append(rate/50.0)
        else:
          if rate>0.3:
            inc_rate_tmp.append(math.pow(1.21,(i+1))*rate)
          else:
            inc_rate_tmp.append(rate)

  if DEBUG:
    print inc_rate_tmp
    print "sum of above:",sum(inc_rate_tmp)
    print "sum click counts",sum_counts
  if sum(inc_rate_tmp)>0.290 :
    limit_to1=sum(inc_rate_tmp)*math.log10(sum_counts)
    inc_marks[word]=[limit_to1,data]
    return True
  else:
    return False

def calc_CV(vlist):
  return standard_deviation(vlist)/average(vlist)

def standard_deviation(vlist):
  total = len(vlist)
  avg=average(vlist)
  dsum=0.0
  for i in vlist:
    dsum+= float(i-avg)*float(i-avg)
  return math.sqrt(dsum/float(total))


def average(vlist):
  total=len(vlist)
  tsum=0.0
  
  for i in vlist:
    tsum+=i
  try:
    r=tsum/float(total)
  except:
    raise Exception(vlist,tsum,total)
  return r

def sortdict(adict):
  return sorted(adict.iteritems(), key=itemgetter(1), reverse=True)

if __name__=='__main__':
    global DELAY
    try:
      DELAY=int(sys.argv[1])
    except:
      DELAY=1
    line = raw_input()
    cur_line=line.rstrip("\n")
    items = cur_line.split("\t")
    keyword = items[0]
    current_word = keyword
    counts.append("\t".join(items[1:]))
    while True :
      try:
        line = raw_input()
        merge(line)
      except EOFError:
        break
    
    reverse_v2()
    inc_marks=sortdict(inc_marks)
    for i in inc_marks:
      print "%s\t%s\t%s\t%s" % ('i',i[0],i[1][0],i[1][1])
    
    reverse_marks=sortdict(reverse_marks)
    for i in reverse_marks:
      print "%s\t%s\t%s\t%s" % ('r',i[0],i[1][0],i[1][1])
  

