#coding:utf-8

import logging


def Logging(LogFileName):
    '''
    1、在try 中捕捉异常
        logger.exception(msg,_args)
        logger.error(msg,exc_info = True,_args)
    2、常用的日志函数
        logger.error()
        logger.warning()
        logger.debug()
        logger.info()
        logger.fatal()
    :param LogFileName: 输出日志文件名称
    :return: 日志句柄
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(LogFileName)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s || %(levelname)s || %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)

    return logger

