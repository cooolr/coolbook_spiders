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
    url = 'https://www.69shu.com/modules/article/search.php'
    data = 'searchkey={}&searchtype=all'
    headers = {
        'Host': 'www.69shu.com',
        'origin': 'https://www.69shu.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'x-requested-with': 'mark.via',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.69shu.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',    
        'cookie': 'zh_choose=s'
    }
    try:
        r = requests.post(url, data=data.format(quote(search_key,encoding='gb18030')), headers=headers)
    except:
        return []
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()
    soup = BeautifulSoup(text, 'html.parser')
    results = soup.find_all('div', {'class':"newnav"})
    if not results:
        url = 'https://www.69shu.com/' + r.url.split('/')[-1].split('.')[0]
        title = re.findall('<meta property="og:title" content="(.*?)"/>', text)[0]
        author = re.findall('<meta property="og:novel:author" content="(.*?)"/>', text)[0]
        result = [['69shu',url,title,author]]
        return result
    result = []
    for node in results:
        title = node.h3.a.text
        author = node.div.label.text
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
    headers = {
        'Host': 'www.69shu.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'dnt': '1',
        'x-requested-with': 'mark.via',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        #'referer': 'https://www.69shu.com/txt/31477.htm',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'zh_choose=s',
    }
    r = requests.get(home_url, headers=headers)
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        text = r.text.encode(r.encoding).decode()
    soup =BeautifulSoup(text, 'html.parser')
    text = soup.find_all('div', {'class':"catalog"})[1].prettify()
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
    headers = {
    'Host': 'www.69shu.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'dnt': '1',
    'x-requested-with': 'mark.via',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'zh_choose=s',
    }
    r = requests.get(content_url, headers=headers)
    try:
        text = r.text.encode(r.encoding).decode('gb18030')
    except:
        try:
            text = r.text.encode(r.encoding).decode()
        except:
            r.encoding = "gb18030"
            text = r.text
    title = re.findall('<h1.*?>(.*?)</h1>', text)[0]
    title = re.sub('\d*?\.', '', title)
    #content = re.findall('<!--章节内容开始-->(.*?)<!--章节内容结束-->', text, re.S)[0]
    soup =BeautifulSoup(text, 'html.parser')
    content = soup.find_all('div', {'class':"txtnav"})[0].prettify()
    sub = re.findall('<h1.*?<script>.*?</script>.*?</div>', content,re.S)
    if sub:
        content = content.replace(sub[0],'')
    sub = re.findall('<script>.*?</script>.*?</div>', content,re.S)
    if sub:
        content = content.replace(sub[0],'')
    content = re.sub('<script>.*?</script>', '', content, re.S)
    content = re.sub('<div.*?</div>', '', content, re.S)
    content = re.sub(title, '', content).strip()
    content = re.sub(title.replace(' ',''), '', content).strip()
    content = content.replace('\n','')
    content = content.replace('<br/>', '\n')
    content = content.replace('<div class="txtnav">   \n \n','')
    content = content.replace('(本章完)','')
    content = re.sub('\u2003 .*? \n', '\n', content)
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
    data = search("万族之劫")
    print(data)
    exit()
    # 目录...
    directory = get_directory(data[1])
    print(len(directory))
    url = directory[1][0]
    print(url)
    # 正文
    result = get_content(url)
    print(result)
