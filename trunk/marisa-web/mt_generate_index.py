#coding=utf-8
import gc
import re
import xapian
import sys
import time
import string
import os
import codecs
import multiprocessing
from datetime import datetime

#support chinese
reload(sys)
sys.setdefaultencoding('utf-8')


os.environ['XAPIAN_FLUSH_THRESHOLD']='1000000'
MAX_TERM_LENGTH = 64
FREQ=1
CLICK = 2
DATE=3

def create_index(filename,databasePath):
  print "begin read",filename
  if not os.path.exists(databasePath):
    os.makedirs(databasePath)
  database = xapian.WritableDatabase(databasePath, xapian.DB_CREATE_OR_OPEN)
  stemmer=xapian.Stem('english')
  rex=re.compile(r'[0-9]+|[a-zA-Z]+|[\x80-\xff3]{3}')
  lines=open(filename).readlines()
  processed=0
  len_file=len(lines)
  print filename,"read end"
  time_begin=time.time()
  for line in lines:
    try:
      line=line.encode('utf-8')
    except:
      continue
    line_items=line.split('\t')
    document = xapian.Document()
    freq_sortable=xapian.sortable_serialise(float(line_items[3]))
    click_sortable=xapian.sortable_serialise(float(line_items[4]))
    document.add_value(FREQ,freq_sortable)
    document.add_value(CLICK,click_sortable)
    document.add_value(DATE,line_items[1])
    document.set_data(line_items[0])
    terms=rex.findall(line_items[0])
    for term in terms:
      if len(term) > MAX_TERM_LENGTH:
        document.add_term(stemmer(term[:MAX_TERM_LENGTH]))
      else:
        document.add_term(stemmer(term))
    database.add_document(document)
    processed+=1
    del line
    del line_items
    del document
    del freq_sortable
    del click_sortable
    del terms

    if processed%100000==0:
      end=time.time()
      speed=100000/float(end-time_begin)
      print "="*40
      print filename
      print "speed:\t",speed
      print "percent:\t%s %%" %(100.0*(processed/float(len_file)))
      print "time remain:\t %s hours" %( (len_file-processed)/(speed*3600))
      time_begin=time.time()
  
  gc.collect()
  os.system("rm -rf %s" % filename)
  print filename,"end"
if __name__=="__main__":
  begin=time.time()
  non_processed_list=os.listdir('./indexdata')
  non_processed_list.sort()
  print "total files:",len(non_processed_list)
  workers=[]
  date_str=str(datetime.now()).split(' ')[0]
  for filename in non_processed_list:
    databasePath = os.path.abspath('./index_db'+date_str+'/'+filename)
    print "processing file :",filename
    filepath='./indexdata/'+filename
    th=multiprocessing.Process(target=create_index, args=(filepath,databasePath))
    workers.append(th)
    th.start()
    if len(workers)>15:
      for i in workers:
        i.join()
      workers=[]
  end=time.time()
  print "index OK"
  dir_list=os.listdir('./indexdata'+date_str+'/')
  dirs=" "
  for d in dir_list:
    dirs+='./indexdata'+date_str+'/'+d+" "
  cmd="/home/yuebin/bin/bin/xapian-compact -b 16K -F -m %s ./index_data_F_16KB" % dirs
  os.system(cmd)

  print end-begin
