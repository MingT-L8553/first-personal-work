#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2021/2/20 16:52
#@Author: 李明特
#@File  : formatTXT.py


import re
txt = open("comments.txt", "r", encoding='utf-8').read()
chinese_characters = re.compile(u'[\u4e00-\u9fa5]')
res = re.findall(chinese_characters,txt,re.S)
result = ''.join(res)
with open('result_comments.txt','w') as f:
    f.write(result)

