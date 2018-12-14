import requests
import re
from lxml import etree
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['testdb']
mycol = mydb['lagoujob2']


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
cookie = "_ga=GA1.2.931503576.1535092762; user_trace_token=20180824143920-6e9c80b2-a768-11e8-a356-525400f775ce; LGUID=20180824143920-6e9c8b6b-a768-11e8-a356-525400f775ce; LG_LOGIN_USER_ID=7215dc51a0786dbdd6eb52148c2f2e99b1b22e81efe1ec16; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221667a85b1f11187-01e24c71be7302-8383268-2073600-1667a85b1f29a8%22%2C%22%24device_id%22%3A%221667a85b1f11187-01e24c71be7302-8383268-2073600-1667a85b1f29a8%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22m_cf_cpc_baidu_pc%22%7D%7D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; WEBTJ-ID=20181019124256-1668aa22f652b5-01660025f024cf-8383268-2073600-1668aa22f66951; _gid=GA1.2.1588683591.1539924177; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539653872,1539755875,1539924177; LGSID=20181019124255-72364797-d359-11e8-85da-525400f775ce; PRE_UTM=m_cf_cpc_360_pc; PRE_HOST=www.so.com; PRE_SITE=https%3A%2F%2Fwww.so.com%2Fs%3Fsrc%3Dsrp%26ls%3Dsm2162189%26lm_extend%3Dctype%253A31%26q%3D%25E6%258B%2589%25E9%2592%25A9; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpc_360_pc%26m_kw%3D360_cpc_zz_e110f9_265e1f_%25E6%258B%2589%25E9%2592%25A9; _putrc=6196FF38E4CBB754; JSESSIONID=ABAAABAAAIAACBIFA6C0FB9DDC8236D8F07F4655A353638; login=true; unick=%E4%BD%95%E4%BA%9A%E4%B8%9C; gate_login_token=5e3bd3bed20503e68e0675bb8a7f223bc5498e82c645915b; TG-TRACK-CODE=index_navigation; SEARCH_ID=8e18a733d426403c81467ee20ddcd6ce; LGRID=20181019124307-794c8686-d359-11e8-85da-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539924189"
results = re.findall(r'(.*?)=(.*?);',cookie)  # cookies解析成字典格式
COOKIES = {k:v for k ,v in results}

def get_urls(url):
    try:
    	res = requests.get(url=url,headers=HEADERS,cookies=COOKIES)
    except Exception as e:
        print(e)
    html = res.text
    # Xpath 解析
    root = etree.HTML(html)
    p_url = root.xpath('//div[@class="p_top"]/a/@href')  # 职位详情页列表
    return p_url

def parase_url(link):
	job_info = {}
	resp = requests.get(url=link,headers=HEADERS,cookies=COOKIES)
	html = resp.text
	root_html = etree.HTML(html)
	job_request = root_html.xpath('//dd[@class="job_request"]/p/span/text()')
	company_name = root_html.xpath('//h2[@class="fl"]/text()')[0].strip()
	job_company = root_html.xpath('//dl[@class="job_company"]/dd/ul/li/text()[2]')
     #  [' 移动互联网,硬件\n                ', ' D轮及以上\n                ', ' 2000人以上\n                ', 
     #  '\n                                ']
	company_info = [i.strip() for i in job_company]
	company_size = job_company[-1].strip()
	job_name = root_html.xpath('//div[@class="job-name"]/span/text()')[0].strip()
	job_description = root_html.xpath('//dd[@class="job_bt"]/div/p/text()')  # 工作要求以及工作职责
	 # ['20k-40k ', '/北京 /', '经验3-5年 /', '本科及以上 /', '全职']
	job_salery = job_request[0]
	job_area = job_request[1].replace('/','')
	job_experice = job_request[2].replace('/','')
	job_info.update(job_name=job_name,
					job_salery=job_salery,
					job_area=job_area,
					job_experice=job_experice,
					ob_description = job_description,
					company_info=company_info
					)
	print(job_info)
	mycol.insert_one(job_info)
	return job_info

urlc = "https://www.lagou.com/zhaopin/Python/{}/?filterOption=3"
for i in range(1,30):
	print(i)
	url = urlc.format(i)
	print(url)
	urls_list = get_urls(url)
	print(urls_list)
	if urls_list:
		for link in urls_list:
			try:
				parase_url(link)
			except Exception as e:
				raise e
	else:
		continue


	

