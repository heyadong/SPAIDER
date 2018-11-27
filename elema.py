url = 'https://www.ele.me/restapi/shopping/v2/restaurant/category?latitude=29.475748&longitude=106.435423'
import requests
class EleSpydier():

    def __init__(self):
        self.url = 'https://www.ele.me/restapi/shopping/restaurants'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        self.cookies = {'ubt_ssid': 'dliyaz1up7vcmn4yyholssd44ags17ur_2018-06-01',
                        'utrace': 'a069eaded8cb5c563979a659c79778de_2018-06-01;',
                        ' eleme__ele_me': '37d393d33a8165533df87091cc1e332e%3Ad1c8b9b9f5895677e3b95b9a11110c939ec6e351',
                        'track_id': '1527833757|320ec8dad1e21c2a26a630af9e9270e12d9b3d8308b5e43982|8cd3cfa5a148baf54606e0cfe7d0e464',
                        'USERID': '271897223',
                        'SID': 'X9TEzFtUAa4jO9C5s3Nko5Kqzh8czThz8YEA'}
        self.data = {
            'latitude': '29.535577',
            'longitude': '106.512368',
            'limit': '24',
            'offset': '24',
            'terminal': 'web'
        }

    def get_content(self):
        res = requests.get(url=self.url, headers=self.headers, cookies=self.cookies, params=self.data)
        return res.json()


def parse_content(contents):
    res_info = list()
    for content in contents:
        res_address = content['address']
        res_name = content['name']
        res_phone = content['phone']
        res_lat_long = {'latitude': content['latitude'],
                        'longtitude': content['longitude']}
        res_fee = content['float_delivery_fee']
        res_info.append(dict(res_address=res_address,
                             res_name=res_name,
                             res_phone=res_phone,
                             res_lat_long=res_lat_long,
                             res_fee=res_fee))
    return res_info


ele = EleSpydier()
# print(res.url)
result = ele.get_content()
print(ele.get_content())
print(len(ele.get_content()))
print(parse_content(result))
