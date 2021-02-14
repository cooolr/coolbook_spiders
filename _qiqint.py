# -*- coding: utf-8 -*-

import re
import requests
from concurrent import futures

def search(keyword):
    """
    搜索小说
    Args:
        keyword (str): 搜索关键词

    Returns:
        result (list): [['书源', '小说目录url', '小说名称', '作者'], ...]
    """
    def get_author(url):
        r = requests.get(url[1])
        text = r.text.encode(r.encoding).decode("utf-8")
        author = re.findall('<meta name="author" content="(.*?)"', text)[0]
        return author

    url = "http://www.qiqint.la/modules/article/search.php"
    try:
        r = requests.post(url, data={"searchkey":keyword})
    except:
        return []
    try:
        text = r.text.encode(r.encoding).decode('utf-8')
    except:
        text = r.text.encode(r.encoding).decode('gb18030')
    result = re.findall('<div class="zhuopin.*?"><a href="(.*?)" title="(.*?)txt下载">', text)
    result = [['qiqint',"http://www.qiqint.la/"+i[0].replace('/txt/xiazai','').replace('.html',''), i[1]] for i in result][:30]
    if not result:return []
    #with futures.ThreadPoolExecutor(len(result)) as executor:
    #    authors = list(executor.map(get_author, result))
    #result = [i+[j] for i,j in zip(result,authors)]
    result = [i+['无名'] for i in result]
    return result


def get_directory(url):
    """
    获取小说目录
    Args:
        url (str): 小说目录url

    Returns:
        result (list): [['文章页url', '章节目录'], ...]
    """
    t = url.split('/')[-1]
    r = requests.get(url)
    try:
        text = r.text.encode(r.encoding).decode('utf-8')
    except:
        text = r.text.encode(r.encoding).decode('gb18030')
    result = re.findall('<dd><a href="(.*?)">(.*?)</a></dd>',text)
    result = [[f"http://www.qiqint.la/{t}/{i[0]}",i[1]] for i in result]
    return result


def get_content(url):
    """
    获取小说正文
    Args:
        url (str): 小说正文url

    Returns:
        result (list): [['章节名称', '正文部分html', '下一页url', '上一页url'], ...]
    """
    r = requests.get(url)
    try:
        text = r.text.encode(r.encoding).decode('utf-8')
    except:
        text = r.text.encode(r.encoding).decode('gb18030')
    title = re.findall('<h1>(.*?)</h1>', text)[0].replace('章节目录', '').strip()
    content = re.findall('<script type="text/javascript">show_d\(\);</script>(.*?)<div class="con_show_r">', text,re.S)[0]
    nextpage = re.findall('<a href="(\d*?\.html)" id="xiazhang">下一章.*?</a>', text)
    lastpage = re.findall('<a href="(\d*?\.html)" id="shangzhang">上一章.*?</a>', text)
    if nextpage:
        nextpage = "/".join(url.split("/")[:-1]) + "/" + nextpage[0]
    else:
        nextpage = "#"
    if lastpage:
        lastpage = "/".join(url.split("/")[:-1]) + "/" + lastpage[0]
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
    result = get_content(url)
    print(result)
