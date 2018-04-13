import requests
import os
from bs4 import BeautifulSoup
from threading import Thread
import time
from io import BytesIO
import uuid
'''
妹子图多线程爬虫
Python 由于GIL（global interpreter lock)机制，解释器在执行时仅允许一个线程执行，
所以Python 对cpu密集型操作的程序并不能提升时间
CPU 密集型（程序运行时，计算时间居多）
IO 密集型（程序运行时，等待时间居多）
'''

cookies = {'safedog-flow-item':'',
            'bdshare_firstime':'1523495667532',
            'UM_distinctid':'162b76b07f121f-04d93952845956-50683974-100200-162b76b07f21bf',
           'CNZZDATA30056528':'cnzz_eid%3D1578969588-1523493306-http%253A%252F%252Fwww.meizitu.com%252F%26ntime%3D1523520527'
           }

# 获取首页
def get_url(html):
    headers = {
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.meizitu.com',
        'If-None-Match': "3e17d5ce4a82d31:104f",
        'Upgrade-Insecure-Requests': '1',
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    req = requests.get(html, headers=headers,cookies=cookies)
    req.encoding = 'gb2312'  # 设置解析编码
    if req.status_code == 200:
        req_html = req.text
        soup = BeautifulSoup(req_html,'html5lib')
        contents = soup.find_all('div', class_="pic")
        for content in contents:
            a_contents = content.find_all('a')
            for a_content in a_contents:
                url = a_content['href']
                yield url
    return None


# 获取图片链接
def get_pic_url(url):
    headers = {
        'Referer': 'http://www.meizitu.com/a/more_1.html',
        'Host': 'www.meizitu.com',
        'If-None-Match': "bac2e0ab2632d31:104f",
        'Upgrade-Insecure-Requests': '1',
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    url_content = requests.get(url=url,headers=headers)
    if url_content.status_code == 200:
        url_contents = url_content.text
        soup = BeautifulSoup(url_contents, 'html5lib')
        p_contents = soup.find_all('div', id='picture')[0]
        img_contents = p_contents.find_all('img')
        for img_content in img_contents:
            img_url = img_content['src']
            yield img_url


def down_load(sid):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = 'http://www.meizitu.com/a/more_{}.html'.format(sid)
    print(url+'开始下载')
    for index_url in get_url(url):
        # pic_path = os.getcwd()+'\picture\\'+index_url.split('/')[-1]
        # if not os.path.exists(pic_path):
        #     os.mkdir(pic_path)
        for pic_url in get_pic_url(index_url):
            try:
                req = requests.get(pic_url,headers=headers)
                content = BytesIO(req.content)
                yield content
            except:
                print('error')
                continue

os.mkdir(os.getcwd() + '\picture')

def save_content(sid):
    print('download '+ str(sid))
    for k in down_load(sid):
        filename = 'picture/'+uuid.uuid4().hex + '.jpg'
        if k:
            with open(filename, 'wb') as file_obj:
                file_obj.write(k.read())
                print(filename+' 下载完成')


class MyThread(Thread):

    def __init__(self, sid):
        Thread.__init__(self)
        self.sid = sid

    def run(self):
        save_content(self.sid)

# 开启多进程,计算运行时间
s_time = time.time()
threads = []
for i in range(1,5):
    t = MyThread(i)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print('end')
e_time = time.time()
print(e_time-s_time)





# url1 = 'http://www.meizitu.com/a/more_2.html'
# url2 = 'http://www.meizitu.com/a/more_3.html'
# print(list(get_url(url1)),list(get_url(url2)))

# 使用多线程的两种方法：
# 1、

# start_time = time.time()
# for i in range(12,13):
#     t = Thread(target=down_load,args=(i,))  # 注意args的值是tuple
#     t.start()
#     t.join()
# print('end')
# end_time = time.time()
# print('时间是', end_time-start_time)


#2  时间是 179.3002474308014
'''
class DownloadThread(Thread):
    def __init__(self,sid):
        Thread.__init__(self)
        self.sid = sid
    # run 固定方法,程序从run开始执行 
    def run(self):
        down_load(self.sid)

# os.mkdir(os.getcwd() + '\picture')  # 创建pic文件夹
# threads = []
start_time = time.time()
for i in range(12,13):
    t = DownloadThread(i)
    t.start()
    t.join()
end_time = time.time()
print('时间是',end_time-start_time)
'''




