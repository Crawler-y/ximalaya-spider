import requests
import random
import time
import urllib
import urllib.request
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool, Lock
import os
"""linux中运行此代码"""

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'www.ximalaya.com',
    'User-Agent': random.choice(UA_LIST)
}
headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ximalaya.com/dq/all/2',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'www.ximalaya.com',
    'User-Agent': random.choice(UA_LIST)
}
headers3 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ximalaya.com/dq/comic/',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'www.ximalaya.com',
    'User-Agent': random.choice(UA_LIST)
}


def get_album_url():
    # 根据分类不同，得到该分类目录下所有页面(84页)所有专辑(每页12个)的链接
    start_urls = ['http://www.ximalaya.com/dq/book/classic{}/'.format(num) for num in range(12, 85)]
    for start_url in start_urls:
        # print(start_url)
        html = requests.get(start_url, headers=headers3).text
        soup = BeautifulSoup(html, 'lxml')
        for item in soup.find_all(class_="albumfaceOutter"):
            global album_url
            album_url.append(item.a['href'])


def get_json_urls_from_page_url(url):
    """
    获取该专辑页面上所有音频的json链接
    """
    page_url = url
    html = requests.get(page_url, headers=headers2).text
    if_another = etree.HTML(html).xpath('//div[@class="pagingBar_wrapper"]/a[last()-1]/@data-page')

    print(len(if_another))

    if len(if_another) == 0:
        print('本频道资源存在 1 个页面')
        print('开始解析1个中的第1个页面')
        res = requests.get(page_url, headers=headers2)
        soup = BeautifulSoup(res.content, "html5lib")
        # 得到音频的id
        mp3_ids = soup.select_one('.personal_body').attrs['sound_ids']
        # 拼成json链接并返回
        json_url = 'http://www.ximalaya.com/tracks/{id}.json'
        urls = [json_url.format(id=i) for i in mp3_ids.split(',')]
        mp3_json_urls.extend(urls)

    elif len(if_another) > 0:
        num = if_another[0]
        print('本频道资源存在' + num + '个页面')
        for n in range(1, int(num) + 1):
            print('开始解析{}个中的第{}个页面'.format(num, n))
            url2 = page_url + '?page={}'.format(n)

            res = requests.get(url2, headers=headers2)
            soup = BeautifulSoup(res.content, "html5lib")
            # 得到音频的id
            mp3_ids = soup.select_one('.personal_body').attrs['sound_ids']
            # 拼成json链接并返回
            json_url = 'http://www.ximalaya.com/tracks/{id}.json'
            urls = [json_url.format(id=i) for i in mp3_ids.split(',')]
            mp3_json_urls.extend(urls)


def get_mp3_from_json_url(json_url):
    """
    访问json链接获取音频名称与下载地址并开始下载
    """
    time.sleep(0.3)
    try:
        mp3_info = requests.get(json_url, headers=headers1, timeout=10).json()
    except Exception as e:
        print(e)
        return
    dir_name = mp3_info['album_title']
    title = mp3_info['album_title'] + '_' + mp3_info['title'] + '.m4a'
    path = mp3_info['play_path']

    # 避免特殊字符文件名异常
    title = title.replace('|', '-')
    title = title.replace('/', '-')
    title = title.replace("?", "_")
    title = title.replace("\\", "_")
    dir_name = dir_name.replace('|', '-')
    dir_name = dir_name.replace('/', '-')
    dir_name = dir_name.replace('?', '-')
    dir_name = dir_name.replace('\\', '-')
    filename = '{}/{}'.format(dir_name, title)
    if not os.path.exists(dir_name):
        print('创建文件夹...')
        os.makedirs(dir_name)
    if os.path.exists(filename):
        print(title + "已下载！")
        return
    try:
        def cbk(m, l, b):
            # 回调函数 @m: 已经下载的数据块 @l: 数据块的大小 @b: 远程文件的大小
            per = 100.0 * m * l / b
            if per > 100:
                per = 100
            print('%.2f%%' % per, title)
        time.sleep(0.1)
        urllib.request.urlretrieve(path, filename, cbk)
        return
    except Exception as e:
        print(e)
        print('other error with', title)
        return


if __name__ == '__main__':
    i = 1
    # 专辑url列表
    album_url = []
    # 每一张专辑的所有MP3的url，每一次新的专辑都要更新一次
    mp3_json_urls = []
    # 调用函数，得到专辑url列表
    get_album_url()
    lock = Lock()

    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]
    # del album_url[0]

    for album in album_url:
        print(i)
        i += 1
        print(album)
        # 先对mp3url列表置空
        mp3_json_urls = []
        # 调用函数，得到每张专辑的所有MP3url列表
        get_json_urls_from_page_url(album)
        with Pool(6) as pool:
            # 多线程调用函数，得到最终结果
            pool = Pool(6)
            pool.map_async(get_mp3_from_json_url, mp3_json_urls)
            pool.close()
            pool.join()
            print('下载完成！')
