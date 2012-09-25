#coding=utf-8
import gc
import re
import xapian
import sys
import time
import string
import os
import codecs
from pymmseg import mmseg
mmseg.dict_load_defaults()
#support chinese
reload(sys)
sys.setdefaultencoding('utf-8')


os.environ['PIAN_FLUSH_THRESHOLD']='1000000'
MAX_TERM_LENGTH = 64
FREQ=1
CLICK = 2
DATE=3
 
databasePath = os.path.abspath('index_db')
if not os.path.exists(databasePath):
  os.mkdir(databasePath)
# set xapian database
database = xapian.WritableDatabase(databasePath, xapian.DB_CREATE_OR_OPEN)
#database=xapian.inmemory_open()
SEARCH_ENQUIRE = xapian.Enquire(database)
rex=re.compile(r'[0-9]+')
if __name__=="__main__":
  begin=time.time()
  begin_tmp=begin
  processed=0
  indexer = xapian.TermGenerator()
  stemmer=xapian.Stem('english')
  indexer.set_stemmer(stemmer)
  non_processed_list=os.listdir('./indexdata')
  non_processed_list.sort()
  print "total files:",len(non_processed_list)
  for filename in non_processed_list:
    print "processing file :",filename
    # store a value, it must be a string
    lines=open('./indexdata/'+filename).readlines()
    counter=0
    len_lines=len(non_processed_list)*len(lines)
    print "lines:",len(lines)
    for line in lines:
      try:
        line=line.encode('utf-8')
      except:
        continue
      line_items=line.split('\t')
      document = xapian.Document()
      #indexer.set_document(document)
      #indexer.index_text(line_items[0])
    
      document.add_value(FREQ,xapian.sortable_serialise(float(line_items[3])))
      document.add_value(CLICK,xapian.sortable_serialise(float(line_items[4])))
      document.add_value(DATE,line_items[1])
      document.set_data(line_items[0])
      #terms=rex.findall(line)
      #only numbers
      #for term in terms:
      #  if len(term) > MAX_TERM_LENGTH:
      #    term=term[:MAX_TERM_LENGTH]
      #  document.add_term(stemmer(term))
      
      algor = mmseg.Algorithm(line_items[0])
      for term in algor:
        if len(term.text) > MAX_TERM_LENGTH:
          document.add_term(stemmer(term.text[:MAX_TERM_LENGTH]))
        else:
          document.add_term(stemmer(term.text))
      
      database.add_document(document)
      
      processed+=1
      del line
      del line_items
      del document
      if processed%100000==0:
        print "info:\nprocessed: ",processed
        end_tmp=time.time()
        speed=100000/float(end_tmp-begin_tmp)
        print "speed: %s\ncost in current:%s\npercent:%s%%\ntime to end:%s hours\n" %(speed,end_tmp-begin_tmp,100*(processed/float(len_lines)),(len_lines-processed)/(speed*3600.0))
        begin_tmp=time.time()
        database.commit()
        gc.collect()
    gc.collect()
  
  end=time.time()

  print "OK"
  print end-begin
