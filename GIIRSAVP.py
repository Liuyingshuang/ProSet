#coding:utf-8

import os
import sys
import time
import signal
import subprocess
import socket
from threading import Timer
from multiprocessing import Process, Pool


exepath = os.path.dirname(__file__)
# sys.path.append(exepath)
sys.path.append(os.path.join(exepath, './Logging'))
sys.path.append(os.path.join(exepath, './DrawImage'))
sys.path.append(os.path.join(exepath, './DownFile'))

from config import *
# from FtpDownFile import upload, download
from Draw_Prof_Main import DrawProf
from OutLog import Logging

is_timeout = False
def timeout_callback(p):
    is_timeout = True
    print('exe time out call back')
    print(p.pid)
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except Exception as error:
        print(error)

def Run_Popen(command, logger, timeout = 10):
    print('~'*100)
    logger.info(command)
    ret = -1
    socket.setdefaulttimeout(timeout)
    # # 开始起子进程，并对子进程进行监控，超时则异常退出
    p = subprocess.Popen(command, shell=True)
    # p.wait(timeout=timeout)

    # try:
    #     p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    #     logger.info('Process ID : %d' %p.pid)  # 获取进程ID号
    #
    #     # 创建计时器
    #     my_timer = Timer(timeout, timeout_callback, [p])
    #     my_timer.start()
    #     try:
    #         print("start to count timeout; timeout set to be %d \n" %(timeout))
    #         for line in iter(p.stdout.readline, b''):
    #             logger.info(line)
    #             if is_timeout:
    #                 break
    #         for line in iter(p.stderr.readline, b''):
    #             logger.info(line)
    #             if is_timeout:
    #                 break
    #     finally:
    #         my_timer.cancel()
    #         p.stdout.close()
    #         p.stderr.close()
    #
    #         p.wait(timeout=timeout)
    #         p.kill()
    # except subprocess.TimeoutExpired as e:
    #     logger.exception(comm + ' Fail, will return and record this error')

    # 记录进程返回状态
    logger.info('Process recode : ' + str(p.returncode))
    print('~' * 100)
    return ret

def Run(command, logger, timeout = 5*60):
    print('~'*100)
    logger.info(command)
    ret = -1

    def test(comm):
        ret = os.system(comm)
        logger.info('ret:%d' %ret)
    p = Process(target=test, args= (command,))
    p.start()
    p.join(timeout=timeout)
    # logger.info('ret:%d' %ret)
    print('~' * 100)
    return ret

#FY4A-_GIIRS-_N_REGX_1047E_L1-_IRD-_MULT_NUL_20190505060000_20190505061044_016KM_030V1.HDF

if __name__ == '__main__':

    argv = sys.argv
    strfile = argv[1].split("_")
    NUM = strfile[12][0:3]
    start_time = strfile[9]
    end_time = strfile[10]

    logger = Logging('test.log')

    strparam = ' F4AAVPL2APoR_FY4A-_GIIRS-_GRS20190416044500_PONT_%s_R N_REGX_1047E %s %s' %(NUM, start_time, end_time)
    startime = time.time()
    # 廓线反演
    Run(EXEL2APRE+strparam, logger)
    Run(EXEL2A + strparam, logger)
    Run(EXECLD + strparam, logger)
    Run(EXECLR + strparam, logger)
    Run(EXECOMB+ strparam, logger)
    # Run('python test.py', logger)

    endtime = time.time()
    logger.info('Process Cost: %d s' %(endtime-startime))
    # 廓线绘图
    L2AFileName = r'/WORK/home/qx-fy4/PGSDATA/FY4A/GIIRS/L2/L2A/FY4A-_GIIRS-_N_REGX_1047E_L2A_AVP-_MULT_NUL_20190505060000_20190505061044_016KM_030V1.NC'
    L2FileName = r'/WORK/home/qx-fy4/PGSDATA/FY4A/GIIRS/L2/COMB/FY4A-_GIIRS-_N_REGX_1047E_L2-_AVP-_MULT_NUL_20190505060000_20190505061044_016KM_030V1.NC'

    # DrawProf(L2AFileName, L2FileName)


    # NWP插值
    # Run( EXERTM, ' F4ATFCalculR_FY4A-_AGRI--_AFN20160824000000_DISK_001_R N_DISK_1050E 20190919030000 20190919040000')

    print('%'*100)






