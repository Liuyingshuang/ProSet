#coding:utf-8
import os
import sys


UPHOST = '192.168.2.10'
UPUSER = 'qx-data'
UPPWD = 'qixiang@1040_512'
UPPORT = 22

DOWNHOST = '192.168.2.10'
DOWNUSER = 'qx-data'
DOWNPWD = 'qixiang@1040_512'
DOWNPORT = 22

EXEPATH = r'/WORK/home/qx-fy4/PGSWORK/FY4A/GIIRS/EXE'
FontFile = os.path.join(EXEPATH, r'DrawImage/sunsun.ttf')

EXEL2APRE = os.path.join(EXEPATH, 'L2APRE.e')
EXEL2A = os.path.join(EXEPATH, 'L2A.e')
EXECLD = os.path.join(EXEPATH, 'CLD.e')
EXECLR = os.path.join(EXEPATH, 'CLR.e')
EXECOMB = os.path.join(EXEPATH, 'COMB.e')
EXERTM = os.path.join(EXEPATH, 'RTM.e')

ENV = r'module add python/3.7_anaconda'


