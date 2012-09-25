#coding=utf-8
import xapian
import sys
import string
import os

databasePath = os.path.abspath('index_db')

def search(keywords, offset=0, limit=35):
  
  database = xapian.WritableDatabase(databasePath, xapian.DB_CREATE_OR_OPEN)
  enquire = xapian.Enquire(database)
  queryParser = xapian.QueryParser()
  queryParser.set_stemmer(xapian.Stem('english'))
  queryParser.set_database(database)
  queryParser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
  query = queryParser.parse_query(keywords)

  query_list = [query]

  if len(query_list) != 1:
    query = xapian.Query(xapian.Query.OP_AND, query_list)
  else:
    query = query_list[0]

  offset, limit = 0, database.get_doccount()
  enquire.set_query(query)
  matches = enquire.get_mset(offset, limit)
  for match in matches:
    print 'rank=%s, documentID=%s' % (match.rank, match.docid)
    print match.document.get_data()
    print  match.get_value(1)
    print 'Number of documents matching query: %s' % matches.get_matches_estimated()
    print 'Number of documents returned: %s' % matches.size()
  database.close()
  return matches


