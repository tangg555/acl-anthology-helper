# acl-anthology-helper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/static/v1?label=Readme&message=中文&color=red)](/README_zh.md)

To help search, filter, and download papers from 'acl anthology' ([https://aclanthology.org/](https://aclanthology.org/)).

## Main Features
- Retrieve papers from [acl anthology](https://aclanthology.org/).
<br> retrieve directly from website [acl anthology](https://aclanthology.org/).
<br> e.g. ```Retriever.acl(2021, ConfConsts.LONG)``` 
<br> download all papers's info to local ([MySQL database](https://dev.mysql.com/downloads/mysql/)).
<br> e.g. 
<br>```db = AnthologyMySQL(cache_enable=True)```
<br>```db.create_tables()```
<br>```db.load_data()  # load data and put into database``` 
- Import [ABuilder](https://github.com/lizhenggan/ABuilder) to support chain operations for [MySQL](https://dev.mysql.com/downloads/mysql/.
<br> e.g.
<br>```data = ABuilder().table('paper').where({"year": ["in", years_limit]}).where({"venue": ["in", venue_limit]}).query()```
- Filter papers with by keyword.
<br> e.g. ```filtered = papers.filter('title', 'xxx') | papers.filter('abstract', 'xxx')``` 
<br> e.g. ```filtered = papers.and_containing_filter(attr, [keyword1, keyword2])``` 
- Download papers.
<br> e.g. ``` downloader.multi_download(filtered, download_path)``` 
- Local cache available.
- log available.
- statistics available (although I only count the total number of papers).

## Get Started

Download and decompress the code, open a terminal and checkout to the root directory.
run
```python3
pip install requirements.txt
cd tasks
python basic_task.py
``` 
That's it.

## Note

I develop this project by Python 3.6, and it doesn't support python 2.

**homepage**

![](/images/aclanthology.png)

There are many conferences and contents belonging to them. 

Choose one, and we can see papers' list.

![](/images/paper_list.png)

