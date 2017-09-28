#! /usr/bin/env python3
# coding:utf-8

from threading import Thread

import spider.config


class InitializeThread(Thread):
    def __init__(self, url, _spider):
        super(InitializeThread, self).__init__()
        self.url = url
        self.spider = _spider

    def run(self):
        xpath_rules = dict(
                    parents = '//ul[@class="icoNav"]/li'
                )

        html = self.spider.get_response(self.url).content
        xpath_obj_dict = self.spider.parse_xpath(xpath_rules, html)
        threads = []
        for parents_node in xpath_obj_dict['parents'][1:-1]:
            thr = ParseThread(parents_node, self.spider)
            thr.start()
            threads.append(thr)

        for thr in threads:
            thr.join()


class ParseThread(Thread):
    def __init__(self, node, spider):
        super(ParseThread, self).__init__()
        self.node = node
        self.spider = spider

    def run(self):
        threads = []
        rules = dict(
                first_title = './a/text()',
                second_titles = './em/a/text()',
                second_title_links = './em/a/@href',
            )

        kwargs = dict(
            xml_obj=self.node,
        )

        first_title_dic = self.spider.parse_xpath(rules, **kwargs)
        first_base_path = spider.config.FILES_ROOT

        for title in first_title_dic['first_title']:
            file_name = self.spider.make_dir(title, first_base_path)

            for index in range(len(first_title_dic['second_title_links'])):
                second_title = first_title_dic['second_titles'][index]
                self.spider.make_dir(second_title, file_name)








