#! /usr/bin/env python3
# coding:utf-8

import re
import sys
from threading import Thread

import redis


reload(sys)
sys.setdefaultencoding('utf-8')


class _BaseThread(Thread):
    '''
    爬取类似　列表+下一页　规则的页面基类
    '''
    def __init__(self, _spider, *args, **kwargs):
        super(_BaseThread, self).__init__(*args, **kwargs)
        self.db = redis.StrictRedis()
        self.spider = _spider
        self.sub_pattern = re.compile(u'&nbsp;|-| |－|\||　') # 过滤提取内容规则
        self.link = ''

    def set_link(self, link):
        '''
        设置链接
        '''
        self.link = link

    def save_data(self, result_items):
        '''
        数据保存
        '''
        try:
            self.db.sadd('resold', result_items)
            print '[INFO]: %s (已被爬取^_^)' % result_items['title']
        except Exception as e:
            print '[ERROR]: %s' % e


    def parse_link(self, parent_rules, child_rules):
        '''
        解析页面: 主要是先提取父节点, 再从父节点取到对应元素并保存
        :param parent_rules: 含有key为parent_node, next_link的xpath提取规则的字典
        :param child_rules: 要从父节点提取内容的xpath规则
        :return: 存在下一页链接返回True, 否则Fale
        '''
        response = self.spider.get_response(self.link)
        html = response.content if response is not None else ''

        parent_xml = self.spider.parse_xpath(parent_rules, html=html)
        for parent_node in parent_xml.get('parent_node', ''):

            result_items = self.spider.parse_xpath(child_rules, xml_obj=parent_node)
            for key in result_items:
                val_list = result_items[key]
                try:
                    result_items[key] = self.sub_pattern.sub('', val_list[0])
                except Exception as e:
                    print '[ERROR]: %s, %s' % (key, e)
                    result_items[key] = ''

            self.save_data(result_items)

        next_link = parent_xml.get('next_link', [])
        print next_link
        if next_link:
            self.set_link(next_link[0])
            print '[INFO]: 正在爬取第 %s 页' % next_link[0].split('/')[-2]
            return True
        else:
            return False