import os,sys

if not os.path.dirname(__file__) in sys.path[:1]:
      sys.path.insert(0, os.path.dirname(__file__))
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('/home/yuebin/onebox-scripts/marisa-web/')
sys.path.append('/home/yuebin/onebox-scripts/marisa-web/search/memcached')
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

