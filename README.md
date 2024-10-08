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
- Import [ABuilder](https://github.com/lizhenggan/ABuilder) to support chain operations for [MySQL](https://dev.mysql.com/downloads/mysql/).
<br> e.g.
<br>```data = ABuilder().table('paper').where({"year": ["in", years_limit]}).where({"venue": ["in", venue_limit]}).query()```
- Filter papers with by keyword.
<br> e.g. ```filtered = papers.filter('title', 'xxx') | papers.filter('abstract', 'xxx')``` 
<br> e.g. ```filtered = papers.and_containing_filter(attr, [keyword1, keyword2])``` 
- Download papers.
<br> e.g. ``` downloader.multi_download(filtered, download_path)``` 
- Local cache available.
- Log available.
- Statistics available (although I only count the total number of papers).

## Get Started

- Firstly. [MySQL](https://dev.mysql.com/downloads/mysql/) is required. Mine is MySQL 8.
<br>Configurate your MySQL database and add a ```src/configuration/mysql_cfg.py```.
<br>The content of ```src/configuration/mysql_cfg.py``` is as follows:
```python3
class MySQLCFG(object):
    HOST = 'localhost'
    PORT = 3306
    USER = "root"
    PASSWORD = "xxx"
    DB = "xxx"
``` 
Meanwhile, create the corresponding database in your MySQL database.

- Secondly. If you want to use [ABuilder](https://github.com/lizhenggan/ABuilder).
<br>You need to write a ```tasks/database.py``` with configurations of you MySQL.
<br>You can refer to the homepage of [ABuilder](https://github.com/lizhenggan/ABuilder).

- Download and decompress the code, open a terminal and checkout to the root directory.
<br>run

```python3
pip install requirements.txt
cd tasks
python basic_task.py
``` 
If you want to redownload everything, simply delete the cache directory at ```tasks/cache```  or turn off cache by setting ```cache_enable=False```. Then run ```python basic_task.py``` again.

## Note

I develop this project by Python 3.6, and it doesn't support python 2.

**homepage**

![](/images/aclanthology.png)

There are many conferences and contents belonging to them. 

Choose one, and we can see papers' list.

![](/images/paper_list.png)

