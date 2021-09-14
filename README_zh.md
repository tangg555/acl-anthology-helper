# acl-anthology-helper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/static/v1?label=Readme&message=English&color=blue)](/README_zh.md)

acl-anthology-helper的主要目的是快速地从'acl anthology' ([https://aclanthology.org/](https://aclanthology.org/))官网上下载指定论文集中包含某些关键词的论文.

## 主要功能
- 检索[acl anthology](https://aclanthology.org/) 官网中收录的论文。
<br> 直接从网上检索.
<br> e.g. ```Retriever.acl(2021, ConfConsts.LONG)``` 
<br> 将论文保存到本地数据库中([MySQL](https://dev.mysql.com/downloads/mysql/)).
<br> e.g. 
<br>```db = AnthologyMySQL(cache_enable=True)```
<br>```db.create_tables()```
<br>```db.load_data()  # 将数据爬取载入数据库中``` 
- 引入[ABuilder](https://github.com/lizhenggan/ABuilder) 以支持对[MySQL](https://dev.mysql.com/downloads/mysql/) 的链式操作。
<br> e.g.
<br>```data = ABuilder().table('paper').where({"year": ["in", years_limit]}).where({"venue": ["in", venue_limit]}).query()```
- 通过关键词对论文进行过滤。
<br> e.g. ```filtered = papers.filter('title', 'xxx') | papers.filter('abstract', 'xxx')``` 
<br> e.g. ```filtered = papers.and_containing_filter(attr, [keyword1, keyword2])``` 
- 下载所需要的论文。
<br> e.g. ``` downloader.multi_download(filtered, download_path)``` 
- 本地缓存。
- 日志打印。
- 信息采集。

## 快速开始

下载代码，打开终端切换至代码的根目录。
运行
```python3
pip install requirements.txt
cd tasks
python basic_task.py
``` 

## 提示

该项目用 Python 3.6 所写, 不支持 Python 2。

**ACL Anthology官网**

![](/images/aclanthology.png)

可以看到有很多论文集。

打开其中一个可以看到论文列表。

![](/images/paper_list.png)

