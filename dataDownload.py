#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2021/2/17 15:50
#@Author: 李明特
#@File  : dataDownload.py

import requests
import json
import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 获取各集链接
def getUrllinks():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }
    base_url = 'https://v.qq.com'
    first_url = 'https://v.qq.com/x/cover/mzc00200jg5gfcq/u0034zxdhdi.html'
    html = requests.get(first_url, headers=headers).content.decode()
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', {'class': 'mod_episode'})
    link_list = div.find_all_next('a', {'_stat': 'videolist:click'})
    result_link = list()
    for a in link_list:
        result_link.append(base_url + a['href'])
    return result_link


# 获取评论
def getComments(url):
    # 实例化一个Options对象
    chrome_options = Options()
    # 禁止加载图片
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # 创建一个列表，用于记录每一次拖动滚动条后页面的最大高度
    all_window_height =  []
    # 当前页面的最大高度加入列表
    all_window_height.append(driver.execute_script("return document.body.scrollHeight;"))
    n = 0
    while n < 8:
        n += 1
        print(n)
        # 执行拖动滚动条操作
        driver.execute_script("scroll(0,100000)")
        time.sleep(3)
        check_height = driver.execute_script("return document.body.scrollHeight;")
        # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
        if check_height == all_window_height[-1]:
            try:
                # 网页中内嵌了iframe（driver每次只能在一个页面识别，要先进入iframe页面）
                driver.switch_to.frame("commentIframe")
                clickDiv = driver.find_element_by_class_name("comment-short")
                print("找到了")
                clickDiv.click()
                time.sleep(2)
                # 退出iframe
                driver.switch_to.default_content()
            except Exception as e:
                print(e)
                break
        else:
            all_window_height.append(check_height) #如果不想等，将当前页面最大高度加入列表。

    print("已经到达最底部")
    time.sleep(5)
    driver.quit()


def main():
    result_link = getUrllinks()
    for url in result_link[0:1]:
        t = threading.Thread(target=getComments,args=(url,))
        t.start()

if __name__ == '__main__':
    main()


