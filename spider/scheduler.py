#! /usr/bin/env python3
# coding:utf-8

import time
from Queue import Queue as ThreadQueue
from multiprocessing import Queue as ProcessQueue

from handler.initializehandler import InitializeThread
from handler.househandler import RentThread
from runspider import Spider


class SpiderScheduler(object):
    '''
    作用： 调度器，在runserver方法中用来开不同的进程和线程进行任务分配
    '''
    def __init__(self):
        self.links_thread_queue = ThreadQueue()
        self.nodes_process_queue = ProcessQueue()
        self.spider = Spider()

    def runserver(self, url=''):
        threads = []

        # 下载文件初始化线程
        init_thr = InitializeThread(url, self.spider)
        init_thr.start()
        threads.append(init_thr)

        '''
        '''

        rent_thr = RentThread(self.spider)
        rent_thr.start()
        threads.append(rent_thr)

        for t in threads:
            t.join()









