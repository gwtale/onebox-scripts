#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import time

hadoop_retry_times = 1
hadoop_retry_interval = 1
hadoop_timeout = '600000000'

hadoop_home_path = "~/.hadoop/hadoop";
sendmailpath = "/usr/sbin/sendmail"
homepath = os.path.abspath('/home/yuebin/onebox-scripts/page_change_rate')

keepday = 180
clusternum = 12
capacity = '400'

hadoop_reduce_tasks = {'displaycube':'120',}
gsm_server1 = ""
gsm_server2 = ""
errorReceiver = "yuebin"
reportReceiver = "yuebin" 

sos_phone = "-";
error_phone = "-";


def run_hadoop_retry( command, opath = ''):
    for i in range(hadoop_retry_times) :
        if opath != '':
            ret = os.system( hadoop_home_path + "/bin/hadoop dfs -ls " + opath )
            if ret == 0:
                os.system( hadoop_home_path + '/bin/hadoop dfs -rmr ' + opath)
        ret = os.system(command)
        if ret != 0 :
            time.sleep(hadoop_retry_interval)
        else:
            return 0
    return -1
def copy_to_hadoop_retry(command, opath = ''):
    for i in range(hadoop_retry_times) :
        if opath != '':
            ret = os.system( hadoop_home_path + "/bin/hadoop dfs -ls " + opath )
            if ret == 0:
                os.system( hadoop_home_path + '/bin/hadoop dfs -rm ' + opath + '/*')
            else:
                os.system( hadoop_home_path + '/bin/hadoop dfs -mkdir ' + opath )
        ret = os.system(command)
        if ret != 0 :
            time.sleep(hadoop_retry_interval)
        else:
            return 0
    return -1
def run_local_retry( command, opath = ''):
    for i in range(hadoop_retry_times) :
        if opath != '' and opath != '/':
            make_new_out(opath)
        ret = os.system(command)
        if ret != 0 :
            time.sleep(hadoop_retry_interval)
        else:
            return 0
    return -1

def has_hadoop_dir( opath = ''):
    if opath != '':
        ret = os.system( hadoop_home_path + "/bin/hadoop dfs -ls " + opath )
        if ret == 0:
            return True
        else:
            return False
    return False

def has_hadoop_file(path,filename):
    print 'check hadoop file',path,filename
    ret = os.system( hadoop_home_path + "/bin/hadoop dfs -ls " + path + filename )
    if ret == 0:
        return True
    return False

def make_new_out(path):
    if os.path.isdir(path):
        os.system('rm -rf ' + path)
        print 'r: make new out',path,'already exist'
    os.system('mkdir -p ' + path)


def genmd5fordir(path):
    if os.path.isdir(path):
        names = os.listdir(path)
        for n in names:
            fname = path + '/' + n
            if os.path.isdir(fname):
                continue
            command = 'md5sum %s > %s.md5' %(fname,fname)
            if os.system(command) != 0:
                return -1
        return 0
    return -1

def int2datestr( date,diff ):
    if date == None:
        sec = time.time()
    else:   
        sd = time.strptime( date, '%Y%m%d' )
        sec = time.mktime(sd)
    sec = sec - 86400 * diff  # 1 day is 86400 second
    ltime = time.localtime(sec)
    return time.strftime('%Y%m%d',ltime)

def sendmail(title,info,receiver = errorReceiver):
    os.system( 'echo \"%s\" | mail -s \"%s\" %s' %( info,title, receiver) )



