#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'libin'

# Copyright (c) 2019, shinetek.
# All rights reserved.
#
#
# date         author    changes

import ftplib
import fnmatch
import socket
import time
import datetime
import signal
import sys
import os
import subprocess
import glob


if (len(sys.argv) != 1 and len(sys.argv) != 2):
    print "cmd parms wrong! call_erm.py [YYMMDD]"
    print "YYMMDD: The ymd is you want calc to do this day's data. Please like: 20140101."
    print "            If you ignored  YYMMDD, it will use  cur system time."
    sys.exit(1)
    
#sat = sys.argv[1].upper()

HOST = '10.0.65.102'
USER = 'dmzupload'
PWD = 'dmzupload'
CONST_PORT = 22

log_tag = sys.argv[0]
log_tag = log_tag[:-3]

pid = os.getpid()

def Ftp_upload(YMD_patten,DetectorID,satelliteID): 
    ftppath = '/GSICS/DPPS/FY3C/TELE/'
    localpath = '/nas/disk1/DPPS/TELE/FY3C/' + DetectorID + '/'
        
    sat_localpath = localpath + satelliteID + '/image/'
    #sat_localpath = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/image'
    sat_ftppath = ftppath + satelliteID
    if DetectorID == 'Location':
        sat_ftppath = ftppath + DetectorID
    #sat_ftppath = '/GSICS/DPPS/FY3C/TELE/GNOS'
    sat_patten='FY3C_' + satelliteID + '*'+ YMD_patten +'.png'
    #GNOS_patten='FY3C_GNOS*YYYYMMDD.png'         
    Ftp_upload_FTP(sat_localpath,sat_ftppath,sat_patten)    

def Ftp_upload_FTP_bak(local_path,ftp_path,patten):    
    timeout=600 # in seconds 
    socket.setdefaulttimeout(timeout)
    ftp = ftplib.FTP(HOST)  
    ftp.login(user=USER,passwd=PWD)  
    print '### connect ftp server: %s ...'%HOST
    print 'Local_path : %s'%local_path    
    if not os.path.isdir(local_path):    
        return  
    ftp.cwd(ftp_path)
    for file in os.listdir(local_path): 
        print '### upload file1: %s ...'%file   
        src = os.path.join(local_path, file)  
        if os.path.isfile(src):  
            if fnmatch.fnmatch(file,patten):
                ftp.storbinary('STOR ' + file, open(src, 'rb')) 
                print '### upload file2: %s ...'%file   
        elif os.path.isdir(src):  
            try:    
                ftp.mkd(file) 
                print '### mkdir : %s ...'%file   
            except:    
                sys.stderr.write('the dir is exists %s'%file)  
            Ftp_upload_FTP(src, file, patten)  
    ftp.cwd('..')  
def Ftp_upload_FTP(local_path,ftp_path,patten):    
    timeout=600 # in seconds 
    socket.setdefaulttimeout(timeout)
    ftp = ftplib.FTP(HOST)  
    ftp.login(user=USER,passwd=PWD)  
    print '### connect ftp server: %s ...'%HOST
    print 'Local_path : %s'%local_path 
    if not os.path.isdir(local_path):    
        return  
    ftp.cwd(ftp_path)
    #for file in os.listdir(local_path):
    local_file = local_path + patten
    print '### local file: %s ...' %local_file 
    for file in glob.glob(local_file):
        print '### upload file1: %s ...'%file   
        src = os.path.join(local_path, file)  
        ftp.storbinary('STOR %s' %(os.path.basename(file)), open(file, 'rb')) 
        print '### upload file2: %s ...'%src   
    ftp.cwd('..')  
    
# return utc date like : 20131220
def utc_nowdate():
    cur_time=time.strftime('%Y%m%d',time.localtime(time.time()))
    return cur_time
    
def utc_nowtime():
    cur_time=time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
    return cur_time

# Deal with signal.   
def signal_handler(signum, frame):
    msg = ' Recv signal ' + str(signum) + '. exit now. pid=' + str(pid)
    #writelog(log_filename, log_tag, msg)   ####******
    sys.exit(0)
    
# w: overwirte file if mode not set.
def wt_file(file, data, mode = 'w'):
    try:
        fp = open(file, mode)
        #fcntl.flock(fp, fcntl.LOCK_EX)
        fp.write(data)
        #fcntl.flock(fp, fcntl.LOCK_UN)
        fp.close()
    except IOError,e:
        print 'could not write file:',e

#This Function is write log to file
#argv: logfile: the dest log file to write
#          tag : Now use is Process name 
#          data: The log string you want to write
def writelog(logfile, tag, data):
    logfile=logfile + utc_nowdate() + '.log'
    data = '[' + utc_nowtime() + ']`' + tag + '`' + data + '\n'
    wt_file(logfile, data, 'a')

def call_drawAllMaps(ymd,DetectorID,satelliteID,obc_exec_path,idl_path,alive_file,log_filename):
    cmd = idl_path +  obc_exec_path + 'Drawer/Drawer/Drawer.sav -args ' + '\"' + ymd + '\" \"' + DetectorID + '\" \"' + satelliteID+ '\"'
    print cmd 
    writelog(log_filename, log_tag, ': Start the Thread cmd: ' + cmd)
    child = subprocess.Popen(cmd,shell=True)
    pid = child.pid
    print str(pid)
    wt_file(alive_file, utc_nowtime() + '='+ str(pid) )
    returnCode = child.wait()   
    
    print 'returncode:', returnCode
    if returnCode == 0 :
        writelog(log_filename,  log_tag + ': Normal, Draw all picture Success: ' , cmd)
    else:
        writelog(log_filename,  log_tag + ': Error!!! Draw all picture Failure: ' , cmd)
        #sys.exit(1)        

def call_handle(ymd,DetectorID,satelliteID):
    top_path = '/nas/disk1/DPPS/TELE/FY3C/' + DetectorID + '/' + satelliteID + '/'
    #top_path = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/'
    log_path = top_path + 'log/'
    #log_path = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/log/'
    obc_exec_path = '/nas/disk1/DPPS/TELE/FY3C/Handle/exec/'
    obc_hdf_path = top_path + 'output/'
    #obc_hdf_path = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/output/'
    idl_path ='/usr/local/itt/idl/idl/bin/idl -rt='
    obc_input_path = top_path + 'input/'
    #obc_input_path = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/input/'
    alive_file = top_path + 'alive/' + satelliteID + '_alive.txt'    
    #alive_file = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/alive/GNOS_alive.txt'
    log_filename = log_path + satelliteID + '_'
    #log_filename = '/nas/disk1/DPPS/TELE/FY3C/Detector/GNOS/log/GNOS_'
    
    #call_drawAllMaps(ymd,DetectorID,satelliteID,obc_exec_path,idl_path,alive_file,log_filename)
    Ftp_upload(ymd,DetectorID,satelliteID)

# from ftp_download_TELE_FY3C import jobs_list,traceback
jobs_list= (
            ('Detector','ERM'),
            ('Detector','GNOS'),
            ('Detector','IRAS'),
            ('Detector','MWHS'),
            ('Detector','MWRI'),
            ('Detector','MWTS'),
            ('Detector','SBUS'),
            ('Detector','SIM'),
            ('Detector','TMV'),
            ('Detector','TOU'),
            ('Detector','VIRR'),
            ('Location','MWTS'),
            ('Platform','Platform'),
)

import traceback,gc

# main loop
def main():
    #writelog(log_filename, log_tag, ': Program start. pid=' + str(pid))  
    signal.signal(signal.SIGTERM, signal_handler)   
    signal.signal(signal.SIGINT, signal_handler)  
    while True:
        now_time = datetime.datetime.now() + datetime.timedelta(days=-1)
        ymd = now_time.strftime('%Y%m%d')
        print 'start drawing'
        print now_time
        #if now_time.hour == 15 :
        #####Detector
        #ERM
        for d, i in jobs_list:
                try:
                    call_handle(ymd,d,i)
                except:
                    traceback.print_exc()
            # call_handle(ymd,"Detector","ERM")
            # #GNOS
            # call_handle(ymd,"Detector","GNOS")
            # #IRAS
            # call_handle(ymd,"Detector","IRAS")
            # #MWHS
            # call_handle(ymd,"Detector","MWHS")
            # #MWRI
            # call_handle(ymd,"Detector","MWRI")
            # #MWTS
            # call_handle(ymd,"Detector","MWTS")
            # #SBUS
            # call_handle(ymd,"Detector","SBUS")
            # #SIM
            # call_handle(ymd,"Detector","SIM")
            # #TMV
            # call_handle(ymd,"Detector","TMV")
            # #TOU
            # call_handle(ymd,"Detector","TOU")
            # #VIRR
            # call_handle(ymd,"Detector","VIRR")
            # ########Location
            # #MWTS
            # call_handle(ymd,"Location","MWTS")
            # ########Platform
            # #
            # call_handle(ymd,"Platform","Platform")
            # 
            
        print 'sleeping'
        time.sleep(1 * 60 * 60)
if __name__ == '__main__':
    main()
