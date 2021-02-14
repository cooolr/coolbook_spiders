# -*- coding: utf-8 -*-

import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

headers = {
    'authority': 'www.yoduzw.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://www.yoduzw.com',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.yoduzw.com/search',
    'accept-language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
    # 'cookie': 'Hm_lvt_d6c21518da630dd4f86d47c04de176de=1604993308; zh_choose=n; jieqiVisitTime=jieqiArticlesearchTime%3D1604993329; jieqiVisitId=article_articleviews%3D10762%7C15206; Hm_lpvt_d6c21518da630dd4f86d47c04de176de=1604993331; jieqiVisitTime=jieqiArticlesearchTime%3D1604994853'
}

def search(search_key):
    """
    搜索小说
    Args:
        keyword (str): 搜索关键词

    Returns:
        result (list): [['书源', '小说目录url', '小说名称', '作者'], ...]
    """
    global headers
    url = "https://www.yoduzw.com/search"
    data = 'searchkey={}&searchtype=all'
    try:
        r = requests.post(url, data=data.format(quote(search_key)), headers=headers)
    except:
        return []
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()

    title = re.findall('<meta property="og:title" content="(.*?)"/>', text)

    if title and title[0] == search_key:
        author = re.findall('<meta property="og:novel:author" content="(.*?)"/>', text)[0]
        result = [['yoduzw', r.url, title[0], author]]
        return result
    results = re.findall('<li class="pr pb20 mb20" id="hism">.*?</li>', text, re.S)
    result = []
    for node in results:
        url,title = re.findall('<h3 .*?><a href="(.*?)" target="_self" class=".*?" title=".*?">(.*?)</h3>', node)[0]
        title = BeautifulSoup(title,'html.parser').text
        url = 'https://www.yoduzw.com' + url
        author = re.findall('<b class=".*?">(.*?)</b>', node)[0]
        print(111111,url)
        print(222222,author)
        print(333333,title)
    
        # 搜索结果
        result.append(['yoduzw', url, title, author])
    return result


def get_directory(home_url):
    """
    获取小说目录
    Args:
        url (str): 小说目录url

    Returns:
        result (list): [['文章页url', '章节目录'], ...]
    """
    global headers
    r = requests.get(home_url, headers=headers)
    
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()

    node_list = re.findall('<li class=".*?"><a href="(.*?)" class=".*?"><span class=".*?">(.*?)</span></a></li>', text, re.S)
    # node_list = [[i[0], i[1].strip().split(".")[-1]] for i in node_list]
    return node_list

def get_content(content_url):
    """
    获取小说正文
    Args:
        url (str): 小说正文url

    Returns:
        result (list): [['章节名称', '正文部分html', '下一页url', '上一页url'], ...]
    """
    global headers
    r = requests.get(content_url, headers=headers)
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()
    title = re.findall('<h1.*?>(.*?)</h1>', text)[0]
    content = re.findall('<div class="tp"><script>theme\(\)\;</script></div>(.*?)<div class="tb"><script>cation\(\)\;</script></div>', text, re.S)[0]
    content = re.sub('<script>.*?</script>', '', content, re.S)
    content = content.replace('(本章完)','')
    nextpage = re.findall('书签</a><a href="(.*?)">下一章</a>', text)
    nextpage = [i for i in nextpage if '.html' in i]
    lastpage = re.findall('<a href="(.*?)">上一章</a>', text)
    lastpage = [i for i in lastpage if '.html' in i]
    if nextpage:
        nextpage = "https://www.yoduzw.com"+nextpage[0]
    else:
        nextpage = "#"
    if lastpage:
        lastpage = "https://www.yoduzw.com"+lastpage[0]
    else:
        lastpage = "#"
    return title,content,nextpage,lastpage

if __name__ == "__main__":
    # 搜索结果
    data = search("光之子")[0]
    print(data)

    # 目录
    directory = get_directory(data[1])
    print(len(directory))
    print(directory[0])
    # exit()
    url = directory[0][0]
    # # 正文
    result = get_content(url)
    print(result)
