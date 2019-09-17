#coding:utf-8
import os
import time
import signal
import threading

process = []

def KillSubProcess(signum,_):
    global process
    for pid in process:
        print("now kill process %d"%pid)
        os.kill(pid,signal.SIGKILL)

def child():
    while True:
        print("Child process",os.getpid())
        time.sleep(1)

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, KillSubProcess)
    signal.alarm(5)
    for i in range(10):
        newpid  = os.fork()
        if newpid == 0:
            child()
        else:
            process.append(newpid)
            print("Parent process ",os.getpid(),newpid)
    time.sleep(20)
    signal.alarm(0)
    print("Main process exit")


