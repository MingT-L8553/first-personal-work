# first-personal-work
### brief introduction
    爬取腾讯视频《在一起》电视剧共20集的评论信息
    并根据评论信息分词制作词云图
### Completed functions
- 爬取腾讯视频《在一起》电视剧共20集的评论信息
- 使用jieba对评论信息进行分词
- 使用echarts制作词云图
- 在index.html中渲染数据进行词云图展示
- 将html等文件放入ECS通过简易网站展示词云图
### Innovation
- 使用Xshell、Xftp链接云服务器上传文件，建立简易网站对词云图进行展示
### Project structure
>first-personal-work  
>>README.md  
>>dataDownload.py(爬取评论数据)  
>>dataProcessing.py(数据处理)  
>>chart(子文件夹)  
>>>comments.json(所有的评论数据)  
>>>debug.log  
>>>format_json.py(格式化数据)  
>>>index.html(词云图)  
>>>resultData.json(缩略数据)  
>>>js(子文件夹)  
>>>>echarts-wordcloud.js  
>>>>echarts-wordcloud.js.map  
>>>>echarts-wordcloud.min.js  
>>>>echarts-wordcloud.min.js.map  
>>>>echarts.min.js
### 

