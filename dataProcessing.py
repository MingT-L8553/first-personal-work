#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2021/2/20 16:52
#@Author: 李明特
#@File  : dataProcessing.py


import re
import json
import jieba

# 提取所有汉字
def formatTxt():
    sentences = list()
    with open('comments.txt','r',errors='ignore')as f:
        lines = f.readlines()
        for sentence in lines:
            res = re.findall('[\u4e00-\u9fa5]', sentence)
            if len(res) != 0:
                result = ''.join(res)
            else:
                continue
            sentences.append(result)
    with open('format_comments.txt','w') as f:
        for s in sentences:
            f.write(s)

# 分词
def cutWords():
    # 用键值对的方式统计单词
    count = {}
    txt = open('format_comments.txt','r',errors='ignore').read()
    words = jieba.lcut(txt)
    # 获取停用词
    stopwords = [i.strip() for i in open('stop_words.txt', encoding='utf-8').readlines()]
    for word in words:
        # 去除单词和停用词
        if len(word) != 1 and word not in stopwords:
            count[word] = count.get(word, 0) + 1
        else:
            continue
    return count

# 保存为json数据
def changeType(com_dict):
    with open('comments.json','w') as f:
        com_json = json.dumps(com_dict,ensure_ascii=False)
        f.write(com_json)


if __name__ == '__main__':
    formatTxt()
    comments_dict = cutWords()
    changeType(comments_dict)


