# -*- coding:utf-8 -*-

# effect analyse
# @ericyue
# hi.moonlight@gmail.com


def init_vars():
  return {"baidu":0.0,"google":0.0,"qss":0.0,"onebox":0.0,"other":0.0}

#第1-3位点击率
top3_click_counts=init_vars()
pos1_click_counts=init_vars()
pos2_click_counts=init_vars()
pos3_click_counts=init_vars()

time_range_counts=init_vars()
first_click_time=init_vars()

non_click_counts=init_vars()

#翻页率
page_change_counts=init_vars()
page_change_insearch_counts=init_vars()
#换query搜索比例
query_change_counts=init_vars()

total_goals=init_vars()
#首次点击时间间隔

total_search=init_vars()
total_click=init_vars()

def fill_dict(fdict,items):
  fdict['baidu']+=items[1]
  fdict['google']+=items[2]
  fdict['qss']+=items[3]
  fdict['onebox']+=items[4]
  fdict['other']+=items[5]

def merge(line):
  global top3_click_counts
  global pos1_click_counts
  global pos2_click_counts
  global pos3_click_counts
  global time_range_counts
  global first_click_time
  global non_click_counts
  global page_change_counts
  global page_change_insearch_counts
  global query_change_counts
  global total_goals

  items=line.split('\t')
  for i in range(1,6):
      items[i]=float(items[i])

  if items[0]=='time_range_counts':
    fill_dict(time_range_counts,items)    
  elif items[0]=='first_click_time':
    fill_dict(first_click_time,items)    
  elif items[0]=='non_click_counts':
    fill_dict(non_click_counts,items)    
  elif items[0]=='top3_click_counts':
    fill_dict(top3_click_counts,items)    
  elif items[0]=='pos1_click_counts':
    fill_dict(pos1_click_counts,items)    
  elif items[0]=='pos2_click_counts':
    fill_dict(pos2_click_counts,items)     
  elif items[0]=='pos3_click_counts':
    fill_dict(pos3_click_counts,items)
  elif items[0]=='query_change_counts':
    fill_dict(query_change_counts,items)
  elif items[0]=='page_change_counts':
    fill_dict(page_change_counts,items)
  elif items[0]=='page_change_insearch_counts':
    fill_dict(page_change_insearch_counts,items)
  elif items[0]=='total_goals':
    fill_dict(total_goals,items)
  elif items[0]=='total_search':
    fill_dict(total_search,items)    
  elif items[0]=='total_click':
    fill_dict(total_click,items)    

def calc_rate(name,head,bottom):

  for i in head:
    if bottom['baidu']==0.0:
      baidu=0.0
    else:
      baidu=head['baidu']/bottom['baidu']
    if bottom['google']==0.0:
      google=0.0
    else:
      google=head['google']/bottom['google']
    if bottom['qss']==0.0:
      qss=0.0
    else:
      qss=head['qss']/bottom['qss']
    if bottom['onebox']==0.0:
      onebox=0.0
    else:
      onebox=head['onebox']/bottom['onebox']
    if bottom['other']==0.0:
      other=0.0
    else:
      other=head['other']/bottom['other']
  print "%s\t%s\t%s\t%s\t%s\t%s" %(name,baidu,google,qss,onebox,other)
    
if __name__=='__main__':

  while True :
    try:
      line = raw_input().rstrip('\n')
      merge(line)
    except EOFError:
      break

  calc_rate("click_rate",total_click,total_search)
  calc_rate("top3_click_rate",top3_click_counts,total_search)
  calc_rate("pos1_click_rate",pos1_click_counts,total_search)
  calc_rate("pos2_click_rate",pos2_click_counts,total_search)
  calc_rate("pos3_click_rate",pos3_click_counts,total_search)
  calc_rate("first_click_time",first_click_time,time_range_counts)
  calc_rate("non_click_rate",non_click_counts,total_search)
  calc_rate("page_change_rate",page_change_counts,total_search)
  calc_rate("page_change_insearch_rate",page_change_insearch_counts,total_search)
  calc_rate("query_change_rate",query_change_counts,total_search)
  
  tmp=init_vars()
  for i in tmp:
    tmp[i]=1.0
  calc_rate("total_search",total_search,tmp)
  calc_rate("total_click",total_click,tmp)
