#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2021/2/21 14:52
#@Author: 李明特
#@File  : format_json.py

import json
with open('comments.json','r') as f:
    data_dict = json.load(f)
    # 对字典进行排序
    sort_dict = sorted(data_dict.items(),key=lambda d:d[1],reverse=True)
    datas = list()
    # 取前100个关键词
    for i in range(100):
        data = {"name":sort_dict[i][0],"value":str(sort_dict[i][1])}
        datas.append(data)
    # print(datas)
with open('resultData.json','w',encoding='utf-8') as f:
    # 添加参数，ensure_ascii = False ,它默认是True
    json.dump(datas,f,ensure_ascii=False)