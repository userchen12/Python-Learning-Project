import re, random, requests, logging
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool

logging.basicConfig(level=logging.DEBUG)
time_out = 6
count = 0
proxies = []
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
proxy_url = 'https://www.xicidaili.com/'

def GetProxies():
    global proxies
    try:
        res = requests.get(proxy_url, headers=headers)
    except:
        logging.error('Visit failed')
        return
    ht = html.fromstring(res.text)
    raw_proxy_list = ht.xpath('//*[@id="ip_list"]/tbody/tr')
    for item in raw_proxy_list:
        if item.xpath('./td[6]/text()')[0] == 'HTTP':
            proxies.append(
                dict(
                    http='{}:{}'.format(item.xpath('./td[2]/text()')[0],
                                        item.xpath('./td[3]/text()')[0])
                )
            )

#获取博客文章列表
def GetRequests(url,prox):
    res = requests.get(url, headers=headers, proxies=prox, timeout=time_out)
    return res

def GetArticles(url):
    res = GetRequests(url, prox=None)
    html = res.content.decode('utf-8')
    rgx = '<li class="clearfix">.*?<a href="(.*?)" target="_blank">'
    pattern = re.compile(rgx,re.S)
    blog_list = re.findall(pattern, str(html))
    return blog_list

#访问博客
def VisitWithProxy(url):
    proxy = random.choice(proxies)
    GetRequests(url, proxy)

#多次访问
def VisitLoop(url):
    for i in range(count):
        logging.debug('Visiting:\t{}\tfor {} time'.format(url, i))
        VisitWithProxy(url)

if __name__ == '__main__':
    global count
    GetProxies()
    logging.debug('We got {} proxies'.format(len(proxies)))
    BlogUrl = input('Blog Address:'.strip(' '))
    logging.debug('Gonna visit{}'.format(BlogUrl))
    try:
        count = int(input('Visiting Count:'))
    except ValueError:
        logging.error('Arg error')
        quit()
    if count == 0 or count > 200:
        logging.error('Count illegal')
        quit()

    article_list = GetArticles(BlogUrl)
    if len(article_list) == 0:
        logging.error('No articles, error!')
        quit()

    for link in article_list:
        if  'https://blog.csdn.net' not in link:
            link = 'https://blog.csdn.net'+link
        article_list.append(link)

    #多线程
    pool = ThreadPool(int(len(article_list)/4))
    results = pool.map(VisitLoop, article_list)
    pool.close()
    pool.join()
    logging.debug('Task Done')