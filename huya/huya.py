import requests
from lxml import etree
from threading import Thread
from queue import Queue
url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=1'
headers = {
'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'
}
req = requests.get(url=url, headers=headers)
# html = req.content.decode('utf-8')  # charset=utf-8
contents = req.json()
datas = contents['data']['datas']


'''
tree = etree.HTML(html)
live_links = tree.xpath('//li[@class="game-live-item"]/a/@href')  # 选取当前页的直播链接
nums = tree.xpath('//li[@class="game-live-item"]//i[@class="js-num"]/text()')  # 获取直播人数
live_type = tree.xpath('//li[@class="game-live-item"]//span[@class="game-type fr"]//text()')  # 获取直播类型
pes = tree.xpath('//li[@class="game-live-item"]//i[@class="nick"]/text()')  # 主播名称
theme = tree.xpath('//li[@class="game-live-item"]//a[@class="title new-clickstat"]/@title')  # 直播主题
result = list()
for i in range(len(pes)):
    dicts = dict()
    dicts['name'] = pes[i]
    dicts['type'] = live_type[i]
    dicts['watch_num'] = nums[i]
    dicts['theme'] = theme[i]
    dicts['url'] = live_links[i]
    result.append(dicts)
print(result, len(result))
# 按照观看数量从高到低排序
l = sorted(result,
           key=lambda x:int(float(x['watch_num'].split('万')[0])*10000) if x['watch_num'].endswith('万') else int(x['watch_num']),
           reverse=True)
print(l)
'''

#  翻页方式是异步传递json更新数据，直接对页面解析无效，使用chorme 得到翻页时发送的请求连接如下：
#  Request URL: https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=2
#  Request URL: https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=1


def save_content(filename,content):
    import json
    with open(filename,'w+',encoding='utf-8') as file_obj:
        json.dump(content,file_obj,ensure_ascii=False)
        print("保存成功")


def get_per_page(page):
    result = list()
    url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page={}'.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'referer': 'https://www.huya.com/l'
    }
    req = requests.get(url=url,headers=headers)
    contents = req.json()
    datas = contents['data']['datas']
    for data in datas:
        dicts = dict()
        dicts['name'] = data['nick']
        dicts['type'] = data['gameFullName']
        dicts['watchNum'] = data['totalCount']
        dicts['roomName'] = data['introduction']
        dicts['url'] = 'https://www.huya.com/'+data['profileRoom']
        result.append(dicts)
    print("the %s download" %page)
    print(result)
    return result


class Spaider(Thread):
    def __init__(self, id,q):
        super(Spaider, self).__init__()
        self.id = id
        self.q = q

    def run(self):
        self.q.put(get_per_page(self.id))


class Save_thread(Thread):
    def __init__(self, q, file):
        super(Save_thread, self).__init__()
        self.q = q
        self.file = file

    def run(self):
        if self.q.qsize()>0:
            print(self.q.get())
            save_content(filename=self.file,content=self.q.get())

filename = "datas.json"
q = Queue()
thread_list = []  # 线程存放列表
for i in range(1,10):
    t = Spaider(i,q)
    thread_list.append(t)

for t in thread_list:
    t.start()
for t in thread_list:
    t.join()






