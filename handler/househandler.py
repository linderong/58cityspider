#! /usr/bin/env python3
# coding:utf-8

import json
import sys

from handler.basehandler import _BaseThread
from spider import config


reload(sys)
sys.setdefaultencoding('utf-8')


class RentThread(_BaseThread):
    def __init__(self, _spider, *args, **kwargs):
        super(RentThread, self).__init__(_spider, *args, **kwargs)
        self.link = 'http://sz.58.com/chuzu/'

    def save_data(self, result_items):
        '''
        重写父类保存数据方法
        :param result_items: 父类中传递信息以字典形式保存
        '''
        result_json = json.dumps(result_items, ensure_ascii=False)
        with open(config.FILES_ROOT + 'rent.json', 'a') as f:
            f.write(result_json)
            f.write('\n')

    def run(self):
        parent_rules = dict(
            parent_node = '//ul[@class="listUl"]/li', # 每个发布信息父节点
            next_link = '//a[@class="next"]/@href', # 下一页
        )

        child_rules = dict(
            title = './/div[@class="des"]/h2/a/text()', # 标题
            link = './/div[@class="des"]/h2/a/@href', # 链接
            # room　文本有空格注意去空格
            room = './/div[@class="des"]/p[@class="room"]/text()', # 房间规格
            area0 = './/div[@class="des"]/p[@class="add"]/a[1]/text()', # 位置 区
            area1 = './/div[@class="des"]/p[@class="add"]/a[2]/text()', # 位置 楼
            subway = './/div[@class="des"]/p[@class="add"]/text()', # 发布来源
            origin = './/div[@class="des"]/div[@class="jjr"]/span[1]/span[1]/text()', # 租金
            rent = './/div[@class="money"]/b/text()'
        )

        # 一直循环, 知道下一页没有
        while self.parse_link(parent_rules, child_rules):
            pass


class ResoldHouseThread(_BaseThread):
    def __init__(self, _spider, *args, **kwargs):
        super(ResoldHouseThread, self).__init__(_spider, *args, **kwargs)
        self.link = 'http://sz.58.com/ershoufang/'

    def save_data(self, result_items):
        '''
        重写父类保存数据方法
        '''
        result_json = json.dumps(result_items, ensure_ascii=False)
        with open(config.FILES_ROOT + 'resold.json', 'a') as f:
            f.write(result_json)
            f.write('\n')

    def run(self):
        parent_rules = dict(
            parent_node = '//ul[@class="house-list-wrap"]/li',
            next_link='//a[@class="next"]/@href',
        )

        child_rules = dict(
            title='.//h2[@class="title"]/a/text()',
            link='.//h2[@class="title"]/a/@href',
            room='./div[2]/p[1]/span[1]/text()',
            size='./div[2]/p[1]/span[2]/text()',
            orientation = '/div[2]/p[1]/span[3]/text()',
            tier = './div[2]/p[1]/span[4]/text()',
            area0 = './div[2]/p[2]/span[1]/a[1]/text()',
            area1 = './div[2]/p[2]/span[1]/a[2]/text()',
            area2 = './div[2]/p[2]/span[1]/a[3]/text()',
            subway = './div[2]/p[2]/span[2]/text()',
            _from = './div[2]/div[1]/text()',
            price = './div[@class="price"]/p[1]/b/text()',
            uniprice = './div[@class="price"]/p[2]/text()',
        )

        while self.parse_link(parent_rules, child_rules):
            pass

