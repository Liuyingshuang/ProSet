#coding:utf-8
import os
import time
import glob
from pyhdf.SD import *

import urllib.request as request

def checkfile(filename):

    try:
        fin = SD(filename, SDC.READ)
        if len(fin.datasets().keys()) == 0:
            return -1
    except BaseException as e:
        print(e)
        return -1

    return 0

def WriteOK(filename):
    try:
        fo = open(filename, 'w')
        fo.close()
    except BaseException as e:
        print(e)
        return  -1

    return 0


def down1(url, outname):
    print("downloading with urllib")
    request.urlretrieve(url, outname)


def down2(url, outpath):

    outname = os.path.join(outpath, os.path.basename(url).replace('\n',''))
    if not outname.endswith('.hdf'):
        print('file name: %s is error...' %outname)
        return -1

    okname = outname + '.ok'
    if os.path.isfile(okname):
        print('%s is exist, will continue...' %okname)
        return 0

    if os.path.isfile(outname):
        status = checkfile(outname)
        if status != 0:
            print('%s is error file, will download agin...' %outname)
            #os.remove(outname)
        else:
            return 0

    try:
        print('Begin to download %s ...' %outname)
        print(url)
        f = request.urlopen(url,timeout = 5*60) # timeout = 30*60 超出时间限制跳过
        data = f.read()
        with open(outname, "wb") as fout:
            fout.write(data)
            fout.close()

        # WriteOK(okname)
        print('%s is download success...' %outname)
        return 0
    except BaseException as e:
        print(e)
        print('download %s failed...' %outname)
        return -1

    return 0


def down3(url, ):

   pass


def download(strID):
    cmd = r'wget64.exe --no-cookie --tries=5 --no-check-certificate -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3 ' \
          r'https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/%s/ ' \
          r'--header "Authorization: Bearer CB8651DE-9B0B-11E9-A989-D7883D88392C" -P G:\MOD16\2003' %strID
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':

    # stryear = '2013'
    # downtxt = r'./data/MOD04download.txt'
    # outpath = r'./data/%s' %stryear


    '''
    https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD16A2--6/2002-07-01..2002-12-31/DB/70,60,140,0
    2000: 501352726 501352728
    2001: 501352727 501352729
    2002: 501352730 501352731
    2003: 501352732 501352733
    2004: 501352735 501352736
    '''


    '''
    for strID in ['501352735', '501352727']:
        print(strID)
        cmd = r'wget64.exe --no-cookie --tries=5 --no-check-certificate -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3 ' \
          r'https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/%s/ ' \
          r'--header "Authorization: Bearer CB8651DE-9B0B-11E9-A989-D7883D88392C" -P G:\MOD16\2004' %strID
        print(cmd)
        os.system(cmd)

    exit(0)
    '''
    stryear = '2013'

    downtxt = r'./data/MOD04download.txt'
    outpath = r'G:\MOD04\%s' %stryear

    if not os.path.isfile(downtxt):
        print('%s is not exist,will be exit now...' %downtxt)
        exit(-1)

    if not os.path.isdir(outpath):
        print('%s is not exist, will be created...' %outpath)
        os.makedirs(outpath)

    try:
        fin  = open(downtxt, 'r')
        urls = fin.readlines()
        fin.close()
    except BaseException as e:
        print(e)
        exit(1)

    url_all = []

    for item in urls:
        if '.A%s' %stryear in item:
            url_all.append(item)

    for url in url_all:
        print(url)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        st1 = time.time()
        status = 1
        num = 0
        while (num < 5) and (status !=0):
            status = down2(url, outpath)
            num += 1
        st2 = time.time()
        print('%.1fs' %(st2 - st1))








