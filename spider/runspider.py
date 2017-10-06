# -*- coding: utf-8 -*-
import os
import random
import re
import sys

import config
import requests
import redis
from lxml import etree

from utils.proxy import Proxy

reload(sys)
sys.setdefaultencoding('utf-8')


class _Spider(object):
    '''
    发送request请求,　处理response响应
    '''
    def __init__(self):
        self.db = redis.StrictRedis()
        self.headers = config.headers
        self.patterns = re.compile(r'/')
        self.proxy = config.proxy

        if not os.path.exists(config.FILES_ROOT):
            os.mkdir(config.FILES_ROOT)

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()

        return cls._instance

    def user_agent_random(self):
        '''
        随机产生user-agent
        '''
        headers = self.headers
        user_agent = random.choice(config.user_agent_list)

        headers['User-Agent'] = user_agent
        self.headers = headers

    def proxy_random(self):
        '''
        随机代理
        '''
        db = redis.StrictRedis()
        try:
            proxy_list = db.get('proxy')
        except Exception as e:
            print '[ERROR]: proxy查询错误'
            return {}

        if proxy_list is None:
            proxy_list = Proxy().get_pro_ip()

        proxy = random.choice(proxy_list)
        self.proxy = proxy

    def get_response(self, url, method='get', **kwargs):
        '''
        发送请求, 获取response响应
        '''
        self.user_agent_random()

        if method == 'get':
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    # proxy = self.proxy,
                    **kwargs
                )
            except Exception as e:
                print '[ERROR]: 请求错误 %s' % e
                response = None
        elif method == 'post':
            try:
                response = requests.post(url, headers=self.headers, **kwargs )
            except Exception as e:
                response = None
                print '[ERROR]: 请求错误 %s' % e
        else:
            raise NameError

        return response

    def parse_xpath(self, xpath_rules, html='', **kwargs):
        '''
        将提取的xpath规则以字典形式传入，　处理后以字典形式返回
        '''
        xml_obj = kwargs.get('xml_obj', '')
        if xml_obj != '':
            xpath_obj_dict = {}
            for rule_key in xpath_rules:
                xpath_obj_dict[rule_key] = xml_obj.xpath(xpath_rules[rule_key])

            return xpath_obj_dict

        if html == '':
            return {}

        xml_obj = etree.HTML(html)

        xpath_obj_dict = {}
        for rule_key in xpath_rules:
            xpath_obj_dict[rule_key] = xml_obj.xpath(xpath_rules[rule_key])

        return xpath_obj_dict

    def make_dir(self, title, base_path):
        '''
        创建文件夹
        '''
        new_title = self.patterns.sub('', title)

        file_path = base_path + new_title + '/'

        if not os.path.exists(file_path):
            os.mkdir(file_path)
            print '[INFO]: 创建文件夹：%s' % new_title

        return file_path

Spider = _Spider.instance

