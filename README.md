# acl-anthology-helper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

To help search, filter, and download papers from 'acl anthology' ([https://aclanthology.org/](https://aclanthology.org/)).

## Main Features
- Retrieve papers by input conference, content, and year.
<br> e.g. ```Retriever.acl(2021, ConfConsts.LONG)``` 
- filter papers with by keyword in titles, abstract. (containing)
<br> e.g. ```filtered = papers.filter('title', 'xxx') | papers.filter('abstract', 'xxx')``` 
- download them.
<br> e.g. ``` downloader.multi_download(filtered, download_path)``` 
- Local cache available.
- log available.
- statistics available (although I only count the total number of papers).

## Get Started

Download and decompress the code, open a terminal and checkout to the root directory.
run
```python3
pip install requirements.txt
python main.py
``` 
That's it.

## Note

I develop this project by Python 3.6, and it doesn't support python 2.

**homepage**

![](/images/aclanthology.png)

There are many conferences and contents belonging to them. 

Choose one, and we can see papers' list.

![](/images/paper_list.png)

