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

all_chinese_str=ur"[\u4e00-\u9fa5 ]+"
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


sessions={}
#按行读入,每组存入list中
def merge(str1):
  global sessions
  items=str1.split('\t')
  if len(items)!=13:
    return
  if items[6]!='-1' or len(items[2])>100 or items[3] != 'ck' or items[5]=='-' or items[5].find('http') ==-1:
    return
  print "%s\t%s" %(items[2],items[5]) 
if __name__=="__main__":
  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break

  merge("\t")
