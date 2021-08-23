# acl-anthology-helper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

acl-anthology-helper的主要目的是快速地从'acl anthology' ([https://aclanthology.org/](https://aclanthology.org/))官网上下载指定论文集中包含某些关键词的论文.

## 主要功能
- 输入论文集的conference、content和year信息检索论文列表。
<br> 例如输入代码 ```Retriever.acl(2021, ConfConsts.LONG)``` 
- 通过关键词对论文的题目和摘要进行过滤。
<br> 例如输入代码 ```filtered = papers.filter('title', 'xxx') | papers.filter('abstract', 'xxx')``` 
- 下载所需要的论文。
<br> 例如输入代码 ``` downloader.multi_download(filtered, download_path)``` 
- 本地缓存。
- 日志打印。
- 信息采集 （虽然我只记录了论文总数）。

## 快速开始

下载代码，打开终端切换至代码的根目录。
运行
```python3
pip install requirements.txt
python main.py
``` 

## 提示

该项目用 Python 3.6 所写, 不支持 Python 2。

**ACL Anthology官网**

![](/images/aclanthology.png)

可以看到有很多论文集。

打开其中一个可以看到论文列表。

![](/images/paper_list.png)

