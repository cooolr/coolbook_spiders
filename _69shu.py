# -*- coding: utf-8 -*-

import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

def search(search_key):
    """
    搜索小说
    Args:
        keyword (str): 搜索关键词

    Returns:
        result (list): [['书源', '小说目录url', '小说名称', '作者'], ...]
    """
    url = 'https://www.69shu.com/modules/pc/search.php'
    data = 'searchkey={}&searchtype=all&action=%CB%D1%CB%F7'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        r = requests.post(url, data=data.format(quote(search_key,encoding='gb18030')), headers=headers)
    except:
        return []
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()
    soup = BeautifulSoup(text, 'html.parser')
    results = soup.find_all('div', {'class':"sk_xinxi"})
    result = []
    for node in results:
        title = node.h3.a.text
        author = node.p.a.text
        url = node.h3.a['href'].split('/')[-1].split('.')[0]
        url = 'https://www.69shu.com/' + url
        # 搜索结果
        result.append(['69shu', url, title, author])
    return result

def get_directory(home_url):
    """
    获取小说目录
    Args:
        url (str): 小说目录url

    Returns:
        result (list): [['文章页url', '章节目录'], ...]
    """
    r = requests.get(home_url)
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()
    soup =BeautifulSoup(text, 'html.parser')
    text = soup.find_all('div', {'class':"mu_contain"})[1].prettify()
    node_list = re.findall('<a href="(.*?\d)">(.*?)</a>', text, re.S)
    node_list = [[i[0], i[1].strip().split(".")[-1]] for i in node_list]
    return node_list

def get_content(content_url):
    """
    获取小说正文
    Args:
        url (str): 小说正文url

    Returns:
        result (list): [['章节名称', '正文部分html', '下一页url', '上一页url'], ...]
    """
    r = requests.get(content_url)
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        try:
            text = r.text.encode(r.encoding).decode()
        except:
            r.encoding = "gb18030"
            text = r.text
    title = re.findall('<h1>(.*?)</h1>', text)[0]
    title = re.sub('\d*?\.', '', title)
    content = re.findall('<!--章节内容开始-->(.*?)<!--章节内容结束-->', text, re.S)[0]
    content = re.sub('<script>.*?</script>', '', content, re.S)
    content = content.replace('(本章完)','')
    nextpage = re.findall('<a href="(.*?)">下一章</a>', text)
    nextpage = [i for i in nextpage if '.htm' not in i]
    lastpage = re.findall('<a href="(.*?)">上一章</a>', text)
    lastpage = [i for i in lastpage if '.htm' not in i]
    if nextpage:
        nextpage = nextpage[0]
    else:
        nextpage = "#"
    if lastpage:
        lastpage = lastpage[0]
    else:
        lastpage = "#"
    return title,content,nextpage,lastpage

if __name__ == "__main__":
    # 搜索结果
    data = search("遮天")[0]
    # 目录
    directory = get_directory(data[1])
    print(len(directory))
    url = directory[1][0]
    # 正文
    result = get_content("https://www.69shu.com/txt/32027/22950103")
    print(result)
