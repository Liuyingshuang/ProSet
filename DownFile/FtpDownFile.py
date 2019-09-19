#coding:utf-8

import os
import sys

import paramiko
import platform
import stat
sys.path.append(r'../Logging')
from OutLog import Logging



def upload(local, remote, logger):
    '''
    # 上传文件夹 or 文件
    :param local:
    :param remote:
    :return:
    '''
    # 输出日志信息
    # paramiko.util.log_to_file(LogFileName)
    try:
        # 连接到IP地址
        trans = paramiko.Transport((UPHOST, int(UPPORT)))

        # 登录
        trans.connect(username=UPUSER, password=UPPWD, timeout = 10)

        # 建立FTP通道
        sftp = paramiko.SFTPClient.from_transport(trans)
    except BaseException as e:
        logger.exception('')
        return
    # 判断远程端目录是否存在，如果不存在，则创建
    if os.path.isdir(remote):
        try:
            sftp.mkdir(remote)
        except Exception as e:
            logger.error('{} {} {}'.format('mkdir', remote, 'fail, dir is exists'), exc_info = True)
            return


    try:
        if os.path.isdir(local):  # 判断本地参数是目录还是文件
            logger.info('Now, star to upload dir')
            for root, dirs, files in os.walk(local):  # 遍历本地目录
                for file_name in files:
                    local_file_path = os.path.join(root, file_name)
                    # 切片：windows路径去掉盘符
                    if (platform.system() == 'Windows'):
                        remote_file_path = os.path.join(remote, local_file_path[3:])
                    else:
                        remote_file_path = os.path.join(remote, local_file_path)
                    remote_file_path = remote_file_path.replace("\\", "/")

                    try:
                        sftp.put(local_file_path, remote_file_path)
                    except Exception as e:
                        logger.exception('{} {} {} {} {}'.format('put', local_file_path, 'to', remote_file_path, 'fail'))
                    sftp.mkdir(os.path.dirname(remote_file_path))
                    sftp.put(local_file_path, remote_file_path)
            for dir_name in dirs:
                local_dir = os.path.join(root, dir_name)
                # 切片：windows路径去掉盘符
                if (platform.system() == 'Windows'):
                    remote_path = os.path.join(remote, local_dir[3:])
                else:
                    remote_path = os.path.join(remote, local_dir)
                remote_path = remote_path.replace("\\", "/")

                try:
                    sftp.mkdir(os.path.dirname(remote_path))
                    sftp.mkdir(remote_path)
                except Exception as e:
                    logger.exception('{} {} {}'.format('mkdir', remote_path, 'on remote fail'))
        else:
            logger.info('Now, star to upload file')
            try:
                remote_dir, remote_filename = os.path.split(remote)
                local_dir, local_filename = os.path.split(local)

                # remote中没有目标文件名,使用local_filename
                if remote_filename == '' or remote_filename == '.':
                    remote_filename = local_filename
                # remote 中没有目标目录,使用默认目录
                if remote_dir == '':
                    remote_dir = '.'

                try:
                    sftp.chdir(remote_dir)  # 切换到目标目录
                    sftp.put(local, remote_filename)
                except Exception as e:
                    logger.error('{} {}'.format(remote_dir, 'is not exists'), exc_info=True)
            except Exception as e:
                logger.error('{} {} {} {} {}'.format('put', local, 'to', remote, 'fail'), exc_info=True)

    except Exception as e:
        logger.error(exc_info=True)
    finally:
        # 关闭FTP连接
        trans.close()


def download(remote, local, logger):
    # 下载文件 or 目录
    # 输出日志信息
    # paramiko.util.log_to_file(LogFileName)
    try:
        # 连接到IP地址
        trans = paramiko.Transport((DOWNHOST, int(DOWNPORT)))

        # 登录
        trans.connect(username=DOWNUSER, password=DOWNPWD)

        # 建立FTP通道
        sftp = paramiko.SFTPClient.from_transport(trans)
    except Exception as e :
        logger.error( 'connect fail, will be return!!', exc_info=True)
        return
    print(local, remote)

    try:
        # 1.local is file or dir, remote is file
        if stat.S_ISREG(sftp.stat(remote).st_mode):  # remote is file
            local_dir, local_filename = os.path.split(local)
            print(local_dir, local_filename)

            remote_dir, remote_filename = os.path.split(remote)
            print(remote_dir, remote_filename)

            # 如果没有输入文件名使用remote的文件名
            if local_filename == '' and local_filename != '.':
                print('without a filename')
                sftp.get(remote, os.path.join(local, remote_filename))
            else:
                print('have a filename')
                sftp.get(remote, local)
        else:  # remote is dir
            getall(sftp, remote, local)
    except Exception as e:
        logger.error("Download file error", exc_info=True)
    finally:
        trans.close()

def getall(sftp, remote, local):
    print('prarms', remote, local)

    if stat.S_ISREG(sftp.stat(remote).st_mode):
        print(remote, 'is file, get to', os.path.join(local, remote))
        sftp.get(remote, os.path.join(local, remote))
        return
    else:
        print(remote, 'is dir, mkdir at', os.path.join(local, remote))
        os.mkdir(os.path.join(local, remote))
        for f in sftp.listdir_attr(remote):
            getall(os.path.join(remote, f.filename), local)

if __name__ == '__main__':
    logger = Logging('test.log')
    download(r'/WORK/home/qx-data/glb_fcst/gfs/gfs.2019091800', r'/WORK/home/qx-fy4/PGSDATA/FY4A/NWP/wzip', logger)

