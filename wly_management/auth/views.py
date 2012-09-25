#coding=utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
from django.db import connection, transaction
from tools.util import *
import json
from django.template import Context,loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def add_admin(request):
    admin_username=None
    if request.user.is_authenticated():
        admin_username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  

    template = loader.get_template('add_admin.html')
    params= Context({"username":admin_username})
    return HttpResponse(template.render(params))
@login_required
def push_add_admin(request):
    admin_username=None
    if request.user.is_authenticated():
        admin_username=request.user.username

    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    status=""
    try:
        username=request.GET['username']
    except:
        username=None    
    try:
        mail=request.GET['email']
    except:
        mail=None    
    try:
        pwd=request.GET['pwd']
    except:
        pwd=None    
    
    if username != None and mail != None and pwd!=None:
      try:
      
        user = User.objects.create_user(username,mail,pwd)  
        user.is_staff = True
        user.save()
      except:
        return HttpResponse(json.dumps({"status":"添加失败"}))      
      return HttpResponse(json.dumps({"status":"添加成功"}))
    else:
      return HttpResponse(json.dumps({"status":"添加失败"}))
