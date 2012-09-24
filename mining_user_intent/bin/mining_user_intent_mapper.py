#!/usr/bin/python
# -*- coding:utf-8 -*-

# 
# mining user intent 
# @ericyue
#

import time
import sys
import os
import urllib
import urllib2
import re

regx=r"[0-9]{1,4}-[0-9]{1,11}|[0-9]{11}|www|com|net|cn|org|http|\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
skip=re.compile(regx)


current_session={}
current_list=[]

def merge(str1):
  global current_list #store whole sessions(between the empty line) 
  global current_session
  if len(str1.split('\t'))==2:
    analyse()
    current_list=[]
    current_session={}
  else:
    items=str1.split('\t')
    if len(items)!=13:
      return
    current_session['session_id']=items[0]    
    current_session['date']=items[1]
    try:
      query_list=re.findall(ur"[\u4e00-\u9fa5]+|[0-9a-zA-Z]+",items[2].decode('utf-8'))
    except:
      return 
    current_session['query']=' '.join(query_list)
    if len(items[2])<=3:
      current_session={}          
      return
    if skip.search(items[2]):
      current_session={}    
      return
    current_session['action']=items[3]
    current_session['page_num']=items[6]
    current_session['goal_id']=items[9]
    current_session['click_weighing']=items[10]
    current_session['action_num']=items[12]
    current_list.append(current_session)
    current_session={}

def all_the_same(slist):
  current_str=''
  for i in slist:
    if current_str=='':
      current_str=i['query']
      continue
    elif current_str!=i['query']:
      return False
  return True
def all_chinese(str1):
  if re.match(ur"[\u4e00-\u9fa5]+",str1.replace(' ','')):
    return True 
  else:
    return False
def query_similarity(str1,str2):
  if str1=='' or str2 =='':
    return False,0
  try:
    str1_list=re.findall(ur"[\u4e00-\u9fa5]+|[0-9]+|[a-zA-Z]+",str1)
    str2_list=re.findall(ur"[\u4e00-\u9fa5]+|[0-9]+|[a-zA-Z]+",str2)
  except:
    return False,0
  if len(str1_list)==0 or len(str2_list)==0:
    return False,0
  sint=set()
  str1=str1.replace(' ','')
  str2=str2.replace(' ','')
  #去掉有不同版本信息,eg: 3.1.1
  num_version1=re.search(u"[0-9]{1,2}(\.[0-9]{1,2})+",str1)
  num_version2=re.search(u"[0-9]{1,2}(\.[0-9]{1,2})+",str2)
  if num_version1 and num_version2:
    if num_version1.group()==num_version2.group():
      return True,1.11
    else:
      return False,0
  elif num_version1 or num_version2:
    return False,0
  
  #去掉有不同型号信息,eg:g4,gt2022
  version1=re.findall(ur"[a-zA-Z]{1,100}[0-9]{1,100}",str1)
  version2=re.findall(ur"[a-zA-Z]{1,100}[0-9]{1,100}",str2)
  if version1!=[] and version2!=[] and len(version1)==len(version2):
    tmp=version1+version2
    if len(tmp)!=len(set(tmp)):
      return True,1.1
    else:
      return False,-1
  if version1!=[] and version2!=[] and len(version1)!=len(version2):
    return False,-1
  #去掉所有数字限定但不一样的
  num_specify1=re.findall(ur"[0-9]+",str1)
  num_specify2=re.findall(ur"[0-9]+",str2)
  if num_specify1!=[] and num_specify2!=[] and len(num_specify1)==len(num_specify2):
    tmp=num_specify1+num_specify2
    if len(tmp)==len(set(tmp)):
      return False,-1
  if num_specify1!=[] and num_specify2!=[] and len(num_specify1)!=len(num_specify2):
    return False,-1
  elif num_specify1!=[] and num_specify2==[]:
    return False,-1
  elif num_specify1==[] and num_specify2!=[]:
    return False,-1
  #去掉有英文限定但不一致的
  eng_specify1=re.findall(ur"[a-zA-Z]{1,100}",str1)
  eng_specify2=re.findall(ur"[a-zA-Z]{1,100}",str2)
  if eng_specify1!=[] and eng_specify2!=[] and len(eng_specify1)==len(eng_specify2):
    tmp=eng_specify1+eng_specify2
    if len(tmp)==len(set(tmp)):
      return False,-1

  if eng_specify1!=[] and eng_specify2!=[] and len(eng_specify1)!=len(eng_specify2):
    return False,-1
  elif eng_specify1!=[] and eng_specify2==[]:
    return False,-1
  elif eng_specify1==[] and eng_specify2!=[]:
    return False,-1

  numeng_version1=re.findall(ur"[0-9]{1,100}[a-zA-Z]{1,100}",str1)
  numeng_version2=re.findall(ur"[0-9]{1,100}[a-zA-Z]{1,100}",str2)
  if numeng_version1!=[] and numeng_version2!=[] and len(numeng_version1)==len(numeng_version2):
    tmp=numeng_version1+numeng_version2
    if len(tmp)!=len(set(tmp)):
      return True,1.1
    else:
      return False,-1
  if numeng_version1!=[] and numeng_version2!=[] and len(numeng_version1)!=len(numeng_version2):
    return False,-1
  
  if True:
    result=0
    for i in str2_list:
      for j in str1_list:
        if j.find(i)!=-1:
          result+=1
          break
    if result==len(str2_list):
      return True,1
  if True:
    result=0
    for i in str1_list:
      for j in str2_list:
        if j.find(i)!=-1:
          result+=1
          break
    if result==len(str1_list):
      return True,1

  if len(str1)>len(str2):
    for i in str2:
      if str1.find(i)!=-1:
        sint.add(i)
  else:
    for i in str1:
      if str2.find(i)!=-1:
        sint.add(i)
  if len(sint)>1:
    mark= 0.3*max(len(sint)/float(len(str1)),len(sint)/float(len(str2))) + 0.7*min(len(sint)/float(len(str1)),len(sint)/float(len(str2)))
    if mark>0.5001:
      #print mark
      return True,mark
    else:
      return False,0
  else:
    return False,0

def query_list_similarity(str1,result_list):
  result=False
  mark=0
  pos=0
  marks=[]
  poses=[]
  
  for i in range(len(result_list)):
    for j in result_list[i]:
      result,mark=query_similarity(str1,j['query']) 
      if mark==-1:
        break 
      if result:
        marks.append(mark)
        poses.append(i)
  if len(marks)!=0:
    ind=marks.index(max(marks))  
    return True,poses[ind]
  else:
    return False,0

def divide_meaning_groups():
  global current_list
  result_list=[[]]
  result_list[0].append(current_list[0])
  for i in current_list[1:]:
    ret,pos=query_list_similarity(i['query'],result_list)
    if ret==True:
      result_list[pos].append(i)
    else:
      result_list.append([])
      result_list[-1].append(i)
  return result_list 

def dict_to_list(d_dic):
  tmp=[]
  for t in d_dic:
    tmp.append(d_dic[t])
  return tmp

def get_se_ck_br(group):
  se=[]
  ck=[]
  br=[]
  se_dict={}
  ck_dict={}
  br_dict={}

  for i in group:
    if i['action']=='se':
      if i['query'] not in se_dict:
        se_dict[i['query']]=i
    elif i['action']=='ck':
      ck_dict[i['query']]=i
    elif i['action']=='br':
      br_dict[i['query']]=i

  se= dict_to_list(se_dict)
  ck= dict_to_list(ck_dict)
  br= dict_to_list(br_dict)
  
  return se,ck,br

def process_meaning_groups(meaning_group):
  for g in meaning_group:
    se=[]
    ck=[]
    br=[]
    total=[]
    se,ck,br=get_se_ck_br(g)
    if len(se)==0 or len(ck)==0:
      continue
    elif all_the_same(g):
      continue
    else:
      total=se+ck+br
      total.sort(cmp=lambda x,y: cmp(float(x['date']),float(y['date'])))
    #print_result(g)
    merge_meaning_groups(total)
def filter_result(result_set):
  return_set=[]
  return_set.append(result_set[0])
  passwd=False
  marks=0

  version=re.findall(ur"[a-zA-Z]{1,100}[0-9]{1,100}",result_set[0])
  for i in result_set[1:]:
    passwd,marks=query_similarity(result_set[0],i)
    if len(version)!=0:
      #print "version:",result_set[0],i
      if marks==1.1:
        return_set.append(i)
        continue
    else:
      if marks==-1:
        continue
      if passwd:
        return_set.append(i)
      else:
        continue
  return return_set
def last_similarity(key,other):
  if not all_chinese(other) and not all_chinese(key):
    return True
  key_items=key.split(' ')
  other_items=other.split(' ')
  if len(key_items)==1 and len(key)<=10 and len(other_items)!=1:
    if other.find(key)!=-1:
      return True
    else:
      return False
  elif len(key_items)!=1:
    if other.find(key_items[1])==-1:
      return False
    else:
      return True
def merge_meaning_groups(total):
  first_item=total[0]['query']
  result_set=set()
  result_set.add(first_item)
  for i in total[1:]:
    if i['query']!=first_item:
      result_set.add(i['query'])
  result_set=list(result_set)
  if len(result_set)!=0:
    result_set.sort(cmp=lambda x,y: cmp(len(x),len(y)))  
    
    result_set=filter_result(result_set)
  if len(result_set)==0:
    return
  key=result_set[0]
  value=""
  if len(key)<=3:
    return
  for i in result_set[1:]:
    if last_similarity(key,i):
      value+=i+"\t"
  value=value.rstrip('\t')
  if value=='':
    return 
  print "%s\t%s" %(key.encode('utf-8'),value.encode('utf-8'))

def analyse():
  global current_session
  global current_list
  current_list.sort(cmp=lambda x,y: cmp(float(x['date']),float(y['date'])))
  if len(current_list)==1:
    return False
  if all_the_same(current_list):
    return False
  meaning_group=divide_meaning_groups()
  process_meaning_groups(meaning_group)

if __name__=="__main__":
  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break


