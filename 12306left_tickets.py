import requests
import re
import time
import json
#关闭HTTP证书验证警告
requests.packages.urllib3.disable_warnings()

#推送消息
def send_msg(title, info):
    url = 'https://sc.ftqq.com/SCU70172T41d3e1144cbe973133b74e6dcf02d7ef5dfcb403bb73b.' \
          'send?text={}&desp={}'.format(title, info)
    requests.get(url)

#获取并解析12306城市代码文件
def get_station():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?' \
          'station_version=1.9130'
    res = requests.get(url, verify=False)
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)' #\u4e00-\u9fa5是所有汉字的范围
    result = re.findall(pattern, res.text)
    station = dict(result)
    print(station)
    return station

#生成查询12306的URL
def query_12306(station_code,people):
    try:
        date = '2019-12-20'
        from_station_name = '杭州'
        to_station_name = '义乌'
        from_station = station_code[from_station_name]
        to_station = station_code[to_station_name]
        purpose_codes = people
    except:
        date, from_station, to_station, purpose_codes = '--', '--', '--','--'

    #构造url
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
          'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}' \
          '&leftTicketDTO.to_station={}&purpose_codes={}'.format(date,from_station,to_station,purpose_codes)
    print(url)
    return url

def query_train(url,station_code):
    try:
        res = requests.get(url,verify=False)
        raw_trains_info = res.json()['data']['result']
        for raw_train_info in raw_trains_info:
            data_list = raw_train_info.split('|')
            #车次
            train_info = data_list[3]
            #出发站
            from_station_code = data_list[6]
            from_station_name = station_code[from_station_code]
            #终点站
            to_station_code = data_list[7]
            to_station_name = station_code[to_station_code]
            #出发时间
            start_time = data_list[8]
            #到达时间
            arrival_time = data_list[9]
            #总耗时
            last_time = data_list[9]
            #各等座位
            first_class_seat = data_list[31] or '--'
            second_class_seat = data_list[30] or '--'
            soft_seat = data_list[23] or '--'
            hard_seat = data_list[28] or '--'
            no_seat = data_list[26] or '--'

            #查询结果
            info = (
                '车次:{}\n 出发站:{}\n 目的地:{}\n 出发时间:{}\n 到达时间:{}\n 消耗时间:{}\n '
                '座位情况: \n一等座:{}\n 二等座:{}\n 软卧:{}\n 硬卧:{}\n 无座:{}\n\n'.format(
                 train_info,from_station_name,to_station_name,start_time,arrival_time,last_time,
                 first_class_seat,second_class_seat,soft_seat,hard_seat,no_seat
                )
            )
            print(info)
            if second_class_seat and second_class_seat!='无':
                send_msg('{}车有票了'.format(train_info),info)
                return True
            else:
                 continue
    except Exception as e:
        print(e)



if __name__ == '__main__':
    station_code = get_station()
    url = query_12306(station_code, 'ADULT')  # ADULT是成人票，0x00是学生票
    while True:
        time.sleep(1)
        if query_train(url, station_code):
            break

