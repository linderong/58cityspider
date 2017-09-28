#! /usr/bin/env python3
# coding:utf-8
import json
import re
import sys
from multiprocessing import Process
from threading import Thread

from spider import config

reload(sys)
sys.setdefaultencoding('utf-8')


class RentThread(Thread):
    def __init__(self,  _spider):
        super(RentThread, self).__init__()
        self.spider = _spider
        self.pattern = re.compile(r'&nbsp;|-|\||　')
        self.rent_link = 'http://sz.58.com/chuzu/'

    def set_rent_link(self, rent_link):
        self.rent_link = rent_link

    def run(self):
        while True:
            response = self.spider.get_response(self.rent_link)
            html = response.content if response is not None else ''

            xpath_rules = dict(
                parent_node = '//ul[@class="listUl"]/li',
                next_link = '//a[@class="next"]/@href',
            )

            parent_xml = self.spider.parse_xpath(xpath_rules, html=html)
            for parent_node in parent_xml['parent_node']:
                rules = dict(
                    title = './/div[@class="des"]/h2/a/text()',
                    link = './/div[@class="des"]/h2/a/@href',
                    # room　文本有空格注意去空格
                    room = './/div[@class="des"]/p[@class="room"]/text()',
                    area = './/div[@class="des"]/p[@class="add"]/a/text()',
                    origin = './/div[@class="des"]/div[@class="jjr"]/span[1]/span[1]/text()',
                    rent = './/div[@class="money"]/b/text()'
                )

                result_items = self.spider.parse_xpath(rules, xml_obj=parent_node)
                for key in result_items:
                    val_list = result_items[key]
                    try:
                        if key == 'area':
                            s = ''.join(val_list).strip()
                            self.pattern.sub('', s)
                            result_items[key] = s
                        else:
                            result_items[key] = val_list[0].strip().encode('utf-8')
                    except Exception as e:
                        print '[ERROR]:{0}{2},发生异常{1}'.format(key, e, result_items[key])
                        if key == 'origin':
                            break
                else:
                    print '[INFO]: %s (已被爬取^_^)' % result_items['title']
                    item = json.dumps(result_items)
                    with open(config.rent_file_dir + 'rent.json', 'a') as f:
                        f.write(item)
                        f.write('\n')

            next_link = parent_xml['next_link']
            if next_link != []:
                self.set_rent_link(next_link[0])
            else:
                break


