#coding:utf-8
import os
import sys
import datetime
import time
import paramiko
import stat
#######################################
# 秘钥
PKEY = r'../.ssh/id_rsa'
######################################

class FileDownLoad(object):

    def __init__(self, IP=None, PORT=22, USERNAME=None, PWD=None, LogName = None):
        self.ip = IP
        self.port = PORT
        self.username = USERNAME
        self.password = PWD
        if LogName is None:
            LogName = os.path.join('./', '{}.log'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) )

        # self.logger = Logging(LogName)

    def connet(self):
        try:
            if self.password is None:  # 如果没有传入密码，则以秘钥方式登录
                # 指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
                pkey = paramiko.RSAKey.from_private_key_file(PKEY)
                # 建立连接
                self.trans = paramiko.Transport((self.ip, self.port))
                self.trans.connect(username=self.username, pkey=pkey)
                # 将sshclient的对象的transport指定为以上的trans
                self.ssh = paramiko.SSHClient()
                self.ssh._transport = self.trans
                # 实例化一个 sftp对象,指定连接的通道
                self.sftp = paramiko.SFTPClient.from_transport(self.trans)
            else:
                # 连接到IP地址
                self.trans = paramiko.Transport((self.ip, self.port))
                # 登录
                self.trans.connect(username=self.username, password=self.password)
                # 建立FTP通道
                self.sftp = paramiko.SFTPClient.from_transport(self.trans)
        except Exception as e:
            print(e)
            # self.logger.error(GetStrTime() + 'connect fail, will be return!!', exc_info=True)
            # self.logger.error(e)

    def close(self):
        self.trans.close()

    def exec_cmd(self, command):
        # 执行命令，和传统方法一样
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print(stdout.read().decode())

    def DownloadFile(self, remote, local):
        '''
        下载文件
        :param remote: 全路径 + 文件名
        :param local:  全路径 + 文件名
        :return:
        '''
        if stat.S_ISREG(self.sftp.stat(remote).st_mode):  # remote is file
            filename = os.path.basename(remote)
            remote_filename = remote
            if os.path.isdir(local):
                local_filename = os.path.join(local, filename)
            else:
                local_filename = local

            try:
                self.sftp.get(remote_filename, local_filename)
            except BaseException as e:
                print(e)

        else:
            self.WalkPath(remote, local)

    def WalkPath(self, remote, local):
        '''
        下载该目录下的文件
        :param remote:
        :param local:
        :return:
        '''
        if stat.S_ISREG(self.sftp.stat(remote).st_mode):  # 判断是否为文件
            filename = os.path.basename(remote)
            if os.path.isdir(local):
                local_filename = os.path.join(local, filename)
            else:
                local_filename = local

            # 如果文件存在，则不再下载（避免重复下载）
            if os.path.isfile(local_filename):
                # print(GetStrTime(), '%s is exist, will continue...' %(local_filename))
                return None
            print(GetStrTime(), remote, '-->> is file ,\nwill get to -->>', local_filename)
            try:
                self.sftp.get(remote, local_filename)
                self.WriteOK(local_filename, 1)
                print('Download %s success...' %(local_filename))
                return None
            except BaseException as e:
                self.WriteOK(local_filename, 0)
        else:
            for f in self.sftp.listdir_attr(remote):
                self.WalkPath(os.path.join(remote, f.filename), local)

    def WriteOK(self, local_filename, station = 1):
        '''
        如果成功，则生成OK文件，否则，生成ERROR文件
        :param local_filename: 下载的文件名
        :param station: 下载状态，成功为1， 否则失败
        :return:
        '''
        if station == 1:
            okname = local_filename + '.OK'
        else:
            okname = local_filename + '.ERROR'

        try:
            fp = open(okname, 'w')
            fp.write(GetStrTime() + local_filename)
            fp.write('\n')
            fp.close()
        except BaseException as e:
            print(e)
            # self.logger.error(e)

# 获取实时时间，并做格式化处理
def GetStrTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]:', time.localtime(time.time()))