#数据为链家上沈阳市二手房的数据
import requests
from bs4 import BeautifulSoup
import csv
import json

def get_location(name):
    bdurl = 'http://api.map.baidu.com/geocoding/v3/?address='
    output = 'json'
    ak = ak
    '''
    此处和原链接不同，一是删去了callback参数，删去该参数后返回的才是json格式，
    二是百度API接口更新到V3版本了，格式有了改变
    '''
    url = bdurl+name+'&output={}&ak={}&city={}'.format(output,ak,'杭州市')
    res = requests.get(url)
    res = json.loads(res.text)
    lng = res['result']['location']['lng']
    lat = res['result']['location']['lat']
    if lng:
        return str(lng)+","+str(lat)

def house_info():
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36pvid: 15dd6212-1913-4361-8c37-e0de29ef84d0'}
    raw_url = 'https://hz.lianjia.com/ershoufang/pg'
    url_list = [raw_url+str(i) for i in range(1,101,1)]

    houses_list = []
    for url in url_list:
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        #该页面所有房子的信息
        houses = soup.find('ul',class_='sellListContent').find_all('li')
        for house in houses:
            house_dict = {}
            house_dict['name'] = house.find('div',class_='title').get_text()
            addresses = house.find('div',class_='positionInfo').find_all('a')
            final_address = ''
            for address in addresses:
                final_address += address.get_text()
            house_dict['address'] = final_address
            house_dict['price'] = house.find('div',class_='priceInfo').get_text()
            text = house.find('div',class_='houseInfo').get_text()
            house_dict['house'] = house_info_parse(text)
            house_dict['follow'] = house.find('div',class_='followInfo').get_text()
            house_dict['location'] = get_location(final_address)
            print(house_dict)
            houses_list.append(house_dict)
    return houses_list


def house_info_parse(text):
    info_dict = {}
    info_list = text.split('|')
    if len(info_list) == 7:
        info_dict['style'] = info_list[0]
        info_dict['square'] = info_list[1]
        info_dict['direction'] = info_list[2]
        info_dict['decoration'] = info_list[3]
        info_dict['height'] = info_list[4]
        info_dict['year'] = info_list[5]
        info_dict['kind'] = info_list[6]
        return info_dict
    if len(info_list) == 6:
        info_dict['style'] = info_list[0]
        info_dict['square'] = info_list[1]
        info_dict['direction'] = info_list[2]
        info_dict['decoration'] = info_list[3]
        info_dict['height'] = info_list[4]
        info_dict['year'] = 'null'
        info_dict['kind'] = info_list[-1]
        return info_dict

if __name__ == '__main__':
    try:
        houses_list = house_info()
        file = open(r'C:\Users\Fu\Desktop\cloud\ljesf.csv', 'w', newline='')
        headers = ['name','address','price','house','follow','location']
        writers = csv.DictWriter(file, headers)
        writers.writeheader()
        for house in houses_list:
            print(house)
            writers.writerow(house)
        file.close()
    except Exception as e:
        print(e)
