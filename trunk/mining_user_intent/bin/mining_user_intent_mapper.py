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

all_chinese_str=ur"[\u4e00-\u9fa5]+"
regx_all_chinese_str=re.compile(all_chinese_str)

chinese_or_number_or_alphabet=ur"[\u4e00-\u9fa5]+|[0-9]+|[a-zA-Z]+"
regx_chinese_or_number_or_alphabet=re.compile(chinese_or_number_or_alphabet)

version_str=u"[0-9]{1,2}(\.[0-9]{1,2})+"
regx_version_str=re.compile(version_str)

product_type=ur"[a-zA-Z]{1,100}[0-9]{1,100}"
regx_product_type=re.compile(product_type)

number_str=ur"[0-9]+"
regx_number=re.compile(number_str)

alphabet_str=ur"[a-zA-Z]{1,100}"
regx_alphabet=re.compile(alphabet_str)

number_and_alphabet=ur"[0-9]{1,100}[a-zA-Z]{1,100}"
regx_number_and_alphabet=re.compile(number_and_alphabet)

query_items_str=ur"[\u4e00-\u9fa5]+|[0-9a-zA-Z]+"
regx_query_items_str=re.compile(query_items_str)


current_session={}
current_list=[]
query_click_counts={}

#按行读入,每组存入list中
def merge(str1):
  global current_list #store whole sessions(between the empty line) 
  global current_session
  if len(str1.split('\t'))==2:
    if len(current_list)!=0:
      analyse()
    current_list=[]
    current_session={}
  else:
    items=str1.split('\t')
    if len(items)!=13:
      #损坏的数据
      return
    current_session['session_id']=items[0]    
    current_session['date']=items[1]
    try:
      query_list=regx_query_items_str.findall(items[2].decode('utf-8'))
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

#判断list中的每项query是否相同
def all_the_same(slist):
  current_str=''
  for i in slist:
    if current_str=='':
      current_str=i['query']
      continue
    elif current_str!=i['query']:
      return False
  return True

#判断传入的字符串是否都为汉字
def all_chinese(str1):
  if regx_all_chinese_str.match(str1.replace(' ','')):
    return True 
  else:
    return False

#求两个字符串的相似度
def query_similarity(str1,str2):
  if str1=='' or str2 =='':
    return False,0
  try:
    str1_list=regx_chinese_or_number_or_alphabet.findall(str1)
    str2_list=regx_chinese_or_number_or_alphabet.findall(str2)
  except:
    #含有无法处理的特殊字符
    return False,0
  
  #如果不包含任何汉字、数字、字母则为无效query 
  if len(str1_list)==0 or len(str2_list)==0:
    return False,0
  #去掉有不同版本信息,eg: 3.1.1
  num_version1=regx_version_str.search(str1)
  num_version2=regx_version_str.search(str2)
  if num_version1 and num_version2:
    if num_version1.group()==num_version2.group():
      return True,1.11
    else:
      return False,0
  elif num_version1 or num_version2:
    return False,0
  
  #去掉有不同型号信息,eg:g4,gt2022
  version1=regx_product_type.findall(str1)
  version2=regx_product_type.findall(str2)
  if version1!=[] and version2!=[] and len(version1)==len(version2):
    tmp=version1+version2
    if len(tmp)!=len(set(tmp)):
      return True,1.1
    else:
      return False,-1
  if version1!=[] and version2!=[] and len(version1)!=len(version2):
    return False,-1

  #去掉有数字限定但不一样的
  num_specify1=regx_number.findall(str1)
  num_specify2=regx_number.findall(str2)
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
  eng_specify1=regx_alphabet.findall(str1)
  eng_specify2=regx_alphabet.findall(str2)
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
  
  #数字在前,字母在后的限定
  numeng_version1=regx_number_and_alphabet.findall(str1)
  numeng_version2=regx_number_and_alphabet.findall(str2)

  if numeng_version1!=[] and numeng_version2!=[] and len(numeng_version1)==len(numeng_version2):
    tmp=numeng_version1+numeng_version2
    if len(tmp)!=len(set(tmp)):
      return True,1.1
    else:
      return False,-1
  if numeng_version1!=[] and numeng_version2!=[] and len(numeng_version1)!=len(numeng_version2):
    return False,-1
 
  sint=set()
  str1=str1.replace(' ','')
  str2=str2.replace(' ','')
  
  #计算两个字符串重复度
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
    if mark>0.531:
      return True,mark
    else:
      return False,0
  else:
    return False,0

#判断一个string和一个list是否相关,
#如果相关,返回匹配到的pos,否则返回False
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

#把每条记录按大致语义切分成groups
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

#dict转list
def dict_to_list(d_dic):
  tmp=[]
  for t in d_dic:
    tmp.append(d_dic[t])
  return tmp

#从meaning groups中按用户行为拆分成三个list
def has_ck(group):
  ck=0
  for i in group:
    if i['action']=='ck':
      ck+=1
  return ck
  
#处理meaning groups
def process_meaning_groups(group):
  for g in group:
    ck=has_ck(g)
    #若该group没有点击,则没有无效query
    if ck==0:
      continue
    g.sort(cmp=lambda x,y: cmp(float(x['date']),float(y['date'])))
    merge_meaning_groups(g)

#判断一个query是否出现在一个list中
def cmp_query_list(query,c_list):
  for l in c_list:
    if query==l:
      return True
  return False

#TODO:这个函数暂时没啥用，以后可能会用
def last_similarity(str1,str2):
  #@ericyue
  if all_chinese(str1) and all_chinese(str2):
    key_items=str1.split(' ')
    other_items=str2.split(' ')
    if len(key_items)==1 and len(str1)<=10 and len(other_items)!=1:
      if str2.find(str1)!=-1:
        return True
      else:
        return False
    elif len(key_items)!=1 and len(other_items)==1:
      return False
    elif len(key_items)!=1 and len(other_items)!=1:
      if str2.find(key_items[1])==-1:
        return False
      else:
        return True
    else:
      return True
  else:
    return True
#准备输出
def merge_meaning_groups(total):
  global query_click_counts
  first_item=total[0]['query']
  result_set=[]
  result_set.append(first_item)
  for i in total[1:]:
    if not cmp_query_list(i['query'],result_set):
      result_set.append(i['query'])
  if len(result_set)<=1:
    return
  key=result_set[0]+'#'+str(query_click_counts[result_set[0]])
  value=""
  for i in result_set[1:]:
    if last_similarity(result_set[0],i):
      value+=i+'#'+str(query_click_counts[i])+"\t"
  value=value.rstrip('\t')
  if value != '':
    print "%s\t%s" %(key.encode('utf-8'),value.encode('utf-8'))

#统计点击次数
def click_counts():
  global current_list
  global query_click_counts
  for s in current_list:
    if s['action']=='se' and s['query'] not in query_click_counts:
      query_click_counts[s['query']]=0
    elif s['action']=='ck' and s['query'] in query_click_counts:
      query_click_counts[s['query']]+=1
    elif s['action']=='ck' and s['query'] not in query_click_counts:
      query_click_counts[s['query']]=1
    
#处理每个session list
def analyse():
  global current_session
  global current_list
  current_list.sort(cmp=lambda x,y: cmp(float(x['date']),float(y['date'])))
  if len(current_list)==1:
    return False
  click_counts()
  meaning_group=divide_meaning_groups()
  process_meaning_groups(meaning_group)

if __name__=="__main__":
  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break

  merge("\t")
