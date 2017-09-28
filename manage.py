#! /usr/bin/env python3
# coding:utf-8

import time
import sys
from spider.scheduler import SpiderScheduler

from spider import config


def main():
    if len(sys.argv) != 2 or sys.argv[1] != 'runspider':
        sys.exit('如果想开启爬虫，请输入：python manage.py runsipder')

    start_time = time.time()
    url = config.URL
    spider_scheduler = SpiderScheduler()
    spider_scheduler.runserver(url=url)
    end_time = time.time()
    print '[INFO]: 爬取完毕！　共耗时 %s秒' % (end_time - start_time)


if __name__ == '__main__':
    main()