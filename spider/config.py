# coding: utf-8
import os


URL = 'http://www.sz.58.com' #　爬取网站

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
}

FILES_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Download/') # 文件下载的根目录





user_agent_list = [
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
]


proxy = {}

