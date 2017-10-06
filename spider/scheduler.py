#! /usr/bin/env python3
# coding:utf-8

from Queue import Queue as ThreadQueue
from multiprocessing import Queue as ProcessQueue

from handler.initializehandler import InitializeThread
from handler.househandler import RentThread, ResoldHouseThread
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
        '''
        进程和线程的控制
        '''
        threads = []

        # 下载文件初始化线程
        init_thr = InitializeThread(url, self.spider)
        init_thr.start()
        threads.append(init_thr)

        # 二手房爬取线程
        resold_thr = ResoldHouseThread(self.spider)
        resold_thr.start()
        threads.append(resold_thr)

        # 租房爬取线程
        rent_thr = RentThread(self.spider)
        rent_thr.start()
        threads.append(rent_thr)

        for t in threads:
            t.join()









