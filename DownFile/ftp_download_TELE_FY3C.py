#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'libin'

# Copyright (c) 2019, shinetek.
# All rights reserved.    
#    
#                         
# date         author    changes


import ftplib
import os
import sys
import socket
import time
import datetime
import subprocess
import paramiko
from config import *
from  multiprocessing.dummy import Pool


def utc_nowdate():
    cur_time=time.strftime('%Y%m%d',time.localtime(time.time()))
    return cur_time

def utc_nowtime():
    cur_time=time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
    return cur_time

def wt_file(file, data, mode = 'w'):
    try:
        fp = open(file, mode)
        #fcntl.flock(fp, fcntl.LOCK_EX)
        fp.write(data)
        #fcntl.flock(fp, fcntl.LOCK_UN)
        fp.close()
    except IOError as e:
        print('could not write file:',e)

#This Function is write log to file
#argv: logfile: the dest log file to write
#          tag : Now use is Process name 
#          data: The log string you want to write
def writelog(logfile, tag, data):
    logfile=logfile + utc_nowdate() + '.log'
    data = '[' + utc_nowtime() + ']`' + tag + '`' + data + '\n'
    wt_file(logfile, data, 'a')


def Ftp_download(log_filename, local_path, ftp_path, patten):
    try:
        myftp = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror) as e:
        print('ERROR: connot reach "%s"' % HOST)
        return
    print('*****connected to host "%s"' % HOST)
    
    try:
        myftp.login(user=USER, passwd=PWD)
    except ftplib.error_perm:
        print('ERROR: cannot login by ftpCLP !!!')
        myftp.quit()
        return
    
    try:
        myftp.cwd(ftp_path)
    except ftplib.error_perm:
        print('ERROR: cannot change dir to "%s"' % ftp_path)
        myftp.quit()
        return
    
    print('**** Change to "%s" folder' % ftp_path)
    print(patten)
    li = myftp.nlst(patten)
    if li:    
        for EachFile in li:
            print(EachFile)
            bufsize = 1024
            localfile = local_path + EachFile
            #if os.path.isfile(localfile)==True:
                #print localfile + ' is exit!!!'
                #continue

            # 开始下载相应的文件
            with open(localfile, 'wb') as file_handler:
                err = False
                try:
                    myftp.retrbinary('RETR ' + EachFile, file_handler.write, bufsize)
                except:
                    err = True
                    print(writelog(log_filename,'FTP_ERR',traceback.format_exc()))
                else:
                    print('Finish write file ' ,localfile)
            if err:
                os.remove(localfile)
            
        myftp.quit()
        print('All the file finish download !!!'  )
    else:
        print('There are no file !!!')
        myftp.quit()
        
        
def call_make_AllTime_exec(ymd,path,idl_path,log_filename,alive_file,exec_shortname,DetectorID,satelliteID):
    if os.path.isdir(path)==False:
        print( 'Input dir is error')
        return False
    else:
        dh=os.listdir(path)
        for file in dh:
            if file.find('IFLF3CTmcResult'+ ymd +'.csv.OK') != -1:
                print ymd +' data has been completed '
                return
        log_tag = sys.argv[0]
        log_tag = log_tag[:-3]
    cmd = idl_path  + exec_shortname  + ' -args ' + '\"' + ymd + '\" \"' + DetectorID + '\" \"' + satelliteID+ '\"'
    print(cmd)
    writelog(log_filename, log_tag, ': Start the First cmd: ' + cmd)
    child = subprocess.Popen(cmd,shell=True)
    pid = child.pid
    print(str(pid))
    wt_file(alive_file, utc_nowtime() + '='+ str(pid) )
    returnCode = child.wait()   
    print('returncode:', returnCode)
    if returnCode == 0 :
        writelog(log_filename,  log_tag + ': Normal, Draw all picture Success: ' , cmd)
    else:
        writelog(log_filename,  log_tag + ': Error!!! Draw all picture Failure: ' , cmd)
        #sys.exit(1)  

def call_handle(YMD_patten,DetectorID,satelliteID):
    exec_shortname = '/nas/disk1/DPPS/TELE/FY3C/Handle/exec/Compressor/Compressor/Compressor.sav'
    PassESNTime_ftppath = '/OCSDATA/ORB/PassESN/'
    
    top_path = '/nas/disk1/DPPS/TELE/FY3C/' + DetectorID + '/' + satelliteID + '/'
    obc_exec_path = top_path + 'exec/'
    idl_path ='/usr/local/itt/idl/idl/bin/idl -rt='
    obc_input_path = top_path + 'input/'
    log_path = top_path + 'log/'
    log_filename = log_path + satelliteID + '_'
    alive_file = top_path + 'alive/'+ satelliteID + '_alive.txt'
    sat_ftppath = '/OCSDATA/FY3C/TMC/DAYRES/'
    
    if DetectorID == 'Location':
        satelliteID = 'MWTS_DING_WEI'
    elif DetectorID == 'Platform':
        satelliteID = 'PING_TAI'
    sat_ftppath +=  satelliteID
    
    sat_patten='IFLF3CTmcResult' + YMD_patten +'.csv'
    PassESNTime_patten='IFLOFSFY3CPassESNTime' + YMD_patten
    Ftp_download(log_filename,obc_input_path,PassESNTime_ftppath,PassESNTime_patten)
    Ftp_download(log_filename,obc_input_path,sat_ftppath,sat_patten)
    call_make_AllTime_exec(YMD_patten,obc_input_path,idl_path,log_filename,alive_file,exec_shortname,DetectorID,satelliteID)
    print 'I am sleeping now !!!'
    writelog(log_filename,'sleeping ','')
    

    
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


def main():
    argnum = len(sys.argv)
    while True:
    #减一天
        now_time = datetime.datetime.now()
        now_time = now_time + datetime.timedelta(-1)
        YMD_patten = now_time.strftime('%Y%m%d')
        print YMD_patten
        #if now_time.hour == 3:
        pool = Pool(min(len(jobs_list),2))
        for detector,ins in jobs_list:
            print 'deal with :%s %s %s' % (YMD_patten,detector,ins)
            pool.apply_async(call_handle, args=(YMD_patten,detector,ins))
            #call_handle(YMD_patten,detector,ins)
        pool.close()
        pool.join()
        del pool
        gc.collect()
            
        '''    
        for patten,detector,ins in jobs_list:
            try:
                print 'deal with :%s %s %s' %( ins,detector,patten)
                call_handle(patten,detector,ins)
            except:
                traceback.print_exc(5)
        '''
        
        time.sleep(1 * 60 * 60)
if __name__ == '__main__':
    main()
