#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2021/2/17 15:50
#@Author: 李明特
#@File  : dataDownload.py

import requests
# import threading
import time
import re
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    print("各集链接已爬取成功！正在return")
    return result_link

# 获取每一集的评论的targetid
def getTargetid():
    links = getUrllinks()
    targetid_list = list()
    for link in links:
        # 实例化Option对象
        chrome_options = Options()
        # 把Chrome浏览器设置为静默模式
        # chrome_options.add_argument('--headless')
        # # 禁止加载图片
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
            }
        }
        chrome_options.add_experimental_option('prefs', prefs)
        # 设置引擎为Chrome，在后台默默运行
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(link)
        driver.execute_script("scroll(0,50000)")
        # 显示等待id为commentIframe的元素加载完成
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="commentIframe"]'))
        )
        driver.switch_to.frame("commentIframe")
        iframeDiv = driver.find_element('id','J_CommentTotal').get_attribute('href')   # 裂开，一直用bs4的['href']获取属性值，我说怎么搞不出来。。。
        targetid = iframeDiv[20:]
        targetid_list.append(targetid)
        # 退出iframe
        driver.switch_to.default_content()
        driver.quit()
    print("获取每一集的评论的targetid成功！正在return")
    return targetid_list   # 将会返回20集的评论链接中的targetid

# 生成当前时间戳，作为last_value
def getTime():
    t = time.time()
    return int(round(t * 1000))

# 评论写入txt文档
def writeTXT(com_list):
    with open('comments.txt','w',errors='ignore') as f:
        for comment in com_list:
            f.write(comment)
            f.write('\n')

# 获取评论
def getComments():
    comments_list = list()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }
    # cursor的值就不用传参了，每一集的首个评论地址中cursor值均为0，下一条地址可以在上一条中获取
    cursor = 0
    last_value = getTime()
    targetid_list = getTargetid()
    page = 0
    # 每一集都有唯一一个targetid
    for targetid in targetid_list:
        comments_url = 'https://video.coral.qq.com/varticle/' + targetid + '/comment/v2?callback=_varticle' + targetid + 'commentv2&orinum=10&oriorder=o&pageflag=1&cursor=' + str(cursor) + '&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=' + str(last_value)
        html = requests.get(comments_url,headers = headers).content.decode()
        # 首先获取总评论数，计算需要循环多少次
        comTotal = int(re.findall('"oritotal":(.*?),',html,re.S)[0])
        ranges = math.ceil((comTotal-10)/10)  # 向上取整
        last_value = last_value + 3  # 第二页的最后一个值先加三
        n = 1
        page += 1
        for i in range(ranges):
            print("正在爬取第{}集，第{}页的评论".format(page,n))
            n += 1
            # 获取cursor，获取源码用正则表达式识别last
            cursor = re.findall('"last":"(.*?)"',html,re.S)[0]  # 字符串型
            comments_url = 'https://video.coral.qq.com/varticle/' + targetid + '/comment/v2?callback=_varticle' + targetid + 'commentv2&orinum=10&oriorder=o&pageflag=1&cursor=' + str(
                cursor) + '&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=' + str(last_value)
            last_value += 1  # 第二页之后自增1
            html = requests.get(comments_url,headers=headers).content.decode()
            comments = re.findall('"content":"(.*?)"',html,re.S)   # 这里会返回一个列表，其中有10-30条评论（最初的一页评论每条主评下有两条子评论，之后没有子评论）
            for comment in comments:
                comments_list.append(comment)
    print("-----------------------------")
    print("所有评论爬取完成，正在保存文档")
    # 将评论写入txt文档中
    writeTXT(comments_list)

def main():
    getComments()

if __name__ == '__main__':
    main()



# 获取评论(selenium操作)
# 效率太低，换个方法
'''
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
'''


