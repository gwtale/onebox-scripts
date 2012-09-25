import os,sys

if not os.path.dirname(__file__) in sys.path[:1]:
      sys.path.insert(0, os.path.dirname(__file__))
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('/home/yuebin/onebox-scripts/effect_analyse_system/')
sys.path.append('/home/yuebin/onebox-scripts/effect_analyse_system/overview/memcached')
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

