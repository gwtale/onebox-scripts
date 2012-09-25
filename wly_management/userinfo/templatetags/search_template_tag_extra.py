#coding=utf-8
from django import template
import random
register = template.Library()

@register.filter
def cut_str(str,length):
    is_encode = False
    try:
        str_encode = str.encode('gb18030')
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                str = str_encode.decode('gb18030') + '...'
            except:
                str_encode = str_encode[:-1]
                try:
                    str = str_encode.decode('gb18030') + '...'
                except:
                    is_encode = False
    if not is_encode:
        if length < len(str):
            length = length - 2
            return str[:length] + '...'
    return str


@register.filter
def random_label(str,length):
    rnd=[
    "label",
    "label label-success",
    "label label-warning",
    "label label-important",
    "label label-info",
    "label label-inverse"]
    val=random.uniform(1,1000)
    return rnd[int(val)%6]
@register.filter
def date_to_str(str1):
    return str(str1)
@register.filter
def short_date(str1):
  return str(str1).split(' ')[0]
@register.filter
def state_map(str1):
    if str1==0:
      return '试用'.encode('utf-8')
    elif str1==1:
      return '正常'.encode('utf-8')
    elif str1==-1:
      return '停用'.encode('utf-8')
    elif str1==-2:
      return '非法'.encode('utf-8')
@register.filter
def type_map(str1):
    if str1==0:
      return '微博'.encode('utf-8')
    elif str1==2:
      return 'SEO'.encode('utf-8')
    elif str1==1:
      return 'SEM'.encode('utf-8')
@register.filter
def sex_map(str1):
    if str1==0:
      return '女'.encode('utf-8')
    elif str1==1:
      return '男'.encode('utf-8')
     
@register.filter
def format_date(str1):
  return str(str1).encode('utf-8')    
