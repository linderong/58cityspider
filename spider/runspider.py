# -*- coding: utf-8 -*-
import os
import re
import sys

import config
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')


class Spider(object):
    def __init__(self):
        self.cn = config.CN
        self.proxy = config.proxy
        self.headers = config.headers
        self.patterns = re.compile(r'/')

        if not os.path.exists(config.FILES_ROOT):
            os.mkdir(config.FILES_ROOT)

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()

        return cls._instance

    def user_agent_random(self):
        headers = self.headers
        user_agent = config.user_agent_list
        headers['User-Agent'] = user_agent

    def get_response(self, url, method='get', **kwargs):
        if method == 'get':
            try:
                response = requests.get(url, headers=self.headers, **kwargs)
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
        new_title = self.patterns.sub('', title)

        file_path = base_path + new_title + '/'

        if not os.path.exists(file_path):
            os.mkdir(file_path)
            print '[INFO]: 创建文件夹：%s' % new_title

        return file_path


spider = Spider.instance()


def main():
    url = 'http://www.sz.58.com/'
    spider = Spider()
    spider.spider_scheduler(url)


if __name__ == '__main__':
    main()