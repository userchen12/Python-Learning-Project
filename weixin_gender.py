'''该程序是通过selenium来抓取网页版微信的好友资料并进行性别分类，但是网页版微信上不了'''
from selenium import webdriver
import selenium.webdriver, time, re
from selenium.common.exceptions import WebDriverException
import logging
import matplotlib.pyplot as plt
from collections import Counter

chromedriver_path = r'D:\pycharm\chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path)
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    try:
        driver.get('https://wx.qq.com')
        time.sleep(30)
        logging.debug('Starting traking the page')
        group_elements = driver.find_element_by_xpath('可以通过开发者选项获取')
        group_elements.click()
        group_num = int(str(group_elements.text)[1:-11])
        logging.debug('Group num is {}'.format(group_num))

        gender_dict = {'Male':0, 'Female':0, 'Others':0}
        for i in range(2, group_num+2):
            logging.debug('Now the {}th one'.format(i-1))
            icon = driver.find_element_by_xpath('')
            icon.click()
            gender_raw = driver.find_element_by_xpath('').get_attribute('class')
            if 'women' in gender_raw:
                gender_dict['Female'] += 1
            elif 'man' in gender_raw:
                gender_dict['Male'] += 1
            else:
                gender_dict['Others'] += 1
            myicon = driver.find_element_by_xpath('')
            logging.debug('Now click my icon')
            myicon.click()
            time.sleep(0.8)
            logging.debug('Now click group title')
            group_elements.click()
            time.sleep(0.5)

        print(gender_dict)
        print(gender_dict.items())
        counts = Counter(gender_dict) #Count 起一个计数器的作用
        plt.pie([v for v in counts.values()],
                labels=[k for k in counts.keys()],
                pctdistance=1.1,
                labeldistance=1.2,
                autopct='%1.0f%%')
        plt.show()

    except WebDriverException as e:
        print(e.msg)



