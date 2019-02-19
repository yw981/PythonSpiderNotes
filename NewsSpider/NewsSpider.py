# -*- coding: utf-8 -*-
import os
import sys
# 通过pip install  urllib2也会提示找不到包。
# Pyhton2中的urllib2工具包，在Python3中分拆成了urllib.request和urllib.error两个包。就导致找不到包，同时也没办法安装。
import requests
# import urllib.request
import re
from lxml import etree


def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + ".txt"
    with open(path, "w+", encoding='utf8') as fp:
        for s in slist:
            # s[0].encode("utf8")会让输出变成b'字符utf8编码'
            # fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))
            fp.write("%s\t\t%s\n" % (s[0], s[1]))


def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(
        r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage,
        re.S)
    return mypage_Info


def New_Page_Info(new_page):
    '''Regex(slowly) or Xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert (len(new_items) == len(new_urls))
    return zip(new_items, new_urls)


def Spider(url):
    i = 0
    print("downloading ", url)
    myPage = requests.get(url).content.decode("gbk")
    # myPage = urllib2.urlopen(url).read().decode("gbk")
    myPageResults = Page_Info(myPage)
    # print(myPageResults)
    save_path = "results"
    filename = str(i) + "_" + u"新闻排行榜"
    StringListSave(save_path, filename, myPageResults)
    i += 1
    # myPageResults是列表 [('全站', 'http://news.163.com/special/0001386F/rank_whole.html'),('新闻', 'http://news.163.com/special/0001386F/rank_news.html'),
    for item, url in myPageResults:
        print("downloading ", url)
        new_page = requests.get(url).content.decode("gbk")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        newPageResults = New_Page_Info(new_page)
        filename = str(i) + "_" + item
        StringListSave(save_path, filename, newPageResults)
        i += 1


if __name__ == '__main__':
    print("start")
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print("end")
