# coding: utf-8
import urllib2
import json
import os

import redis
from lxml import etree

BASE_DIR = './'

class Proxy(object):
    '''获取西刺网可以用的免费代理透明代理'''
    def __init__(self):
        self.db = redis.StrictRedis(host='127.0.0.1', port='6379')
        self.url = 'http://www.xicidaili.com/nt/1'
        self.parent_xpath = '//tbody/tr/'
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}

    def get_pro_ip(self):
        request = urllib2.Request(self.url, headers=self.user_agent)
        response = urllib2.urlopen(request)
        html = response.read()
        # print html
        html_handler = etree.HTML(html)
        parents = html_handler.xpath('//table/tr')[1]
        ip_list = []
        for ip in parents.xpath('//td[2]'):
            ip_list.append(ip.text)

        port_list = []
        for port in parents.xpath('//td[3]'):
            port_list.append(port.text)

        type_list = []
        for ip_type in parents.xpath('//td[6]'):
            type_list.append(ip_type.text)

        proxy_list = []
        for i in xrange(0, len(ip_list)):
            proxy = {type_list[i]: '{0}:{1}'.format(ip_list[i], port_list[i])}
            if self.ip_test(proxy):
                proxy_list.append(proxy)

        self.db.setex('proxy', 88640, proxy_list)
        print 'list-----', proxy_list
        return proxy_list

    def ip_test(self, proxy):
        pro_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(pro_handler)
        request = urllib2.Request('http://www.baidu.com/')
        try:
            opener.open(request, timeout=5)
        except Exception as e:
            print e
            print '无效的代理是%s' % str(proxy)
            return False

        print '%s是有效代理' % proxy
        return True
        # proxy = json.dumps(proxy, ensure_ascii=True)
        # with open(BASE_DIR + 'ip.txt', 'a') as f:
        #     f.write(proxy + '\r\n')



def main():
    get_proxy = Proxy()
    get_proxy.get_pro_ip()


if __name__ == '__main__':
    main()