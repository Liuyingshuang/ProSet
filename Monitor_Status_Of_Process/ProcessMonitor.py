#coding:utf-8
# import subprocess
# cmd = ['ping', '10.43.19.90']
# import psutil
# try:
#     subprocess.run(cmd, timeout=5)
# except subprocess.TimeoutExpired as e:
#
#     print(e)
#     print('process ran too long')

# status, output = subprocess.getstatusoutput('ping 10.43.19.90')
#
# print(status)
# print(output)

# try:
#     subprocess.check_call('ping 10.43.19.36')
# except subprocess.TimeoutExpired as e:
#     print(e)

# try:
#     p = subprocess.Popen('curl www.baidu1.com')
#     print(p)
#     print(p.pid)
#     ret = p.wait(timeout=5)
#     print(ret)
#     import  time
#     time.sleep(3)
#     p.kill()
# except subprocess.TimeoutExpired as e:
#     print(e)

