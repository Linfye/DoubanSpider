import requests
from lxml import etree
import random
import time

# 填入用户的 ID，可在浏览器地址栏找到
user = ''

headers = {
    # UA 伪装
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',

    # 填入自己账户的 cookie，否则会跳转至登录界面
    'Cookie': ''
}

movie_list = []
start = "0"

# url1 和 url2 是两个参数，1 是爬电影分数，2 是爬书籍分数（因为一开始只打算写电影的爬虫，后来发现书籍也能爬所以后面变量的名称就难得改了）
url1 = 'https://movie.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=list'.format(user, start)
url2 = 'https://book.douban.com/people/{}/collect?sort=time&start={}&filter=all&mode=list'.format(user, start)

# 改参数，默认 url1
page_text = requests.get(url=url1, headers=headers).text
tree = etree.HTML(page_text)
movie_list_e = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/ul/li')
movie_list.append(movie_list_e)

while movie_list_e != []:
    start = str(int(start)+30)
    url1 = 'https://movie.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=list'.format(user, start)
    url2 = 'https://book.douban.com/people/{}/collect?sort=time&start={}&filter=all&mode=list'.format(user, start)

    # 改参数，默认 url1
    page_text = requests.get(url=url1, headers=headers).text
    tree = etree.HTML(page_text)
    movie_list_e = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/ul/li')
    movie_list.append(movie_list_e)

# 不知道为什么，列表最后有一个空值，这里把这个空值 pop 掉
movie_list.pop()

# 解析该用户的分数
movie_url_list = []
movie_name_list = []
movie_star_list = []

for movie_list_e in movie_list:
    for movie in movie_list_e:
        movie_url = movie.xpath('./div[1]/div[1]/a/@href')[0]
        movie_url_list.append(movie_url)

        movie_name = movie.xpath('./div[1]/div[1]/a/text()')[0].strip()
        movie_name_list.append(movie_name)

        if movie.xpath('./div[1]/div[2]/span/@class') != []:
            movie_star = movie.xpath('./div[1]/div[2]/span/@class')[0]
            movie_star_list.append(movie_star)

    """ print(movie_url_list)
    print(movie_name_list)
    print(movie_star_list) """

    user_socre_list = []
    for i in movie_star_list:
        user_score = int(i[6]) * 2
        user_socre_list.append(user_score)

print("用户平均打分为：\n", sum(user_socre_list)/len(user_socre_list))

# 爬豆瓣分数，最好不要一起运行这段代码，这段要爬很久，推荐使用 jupyter notebook
douban_rating_list = []
for douban_url in movie_url_list:

    # 这里防止被豆瓣反爬，取消注释大概是四秒爬一个，注释掉是一秒爬一个
    # time.sleep(random.randint(1, 4))
    url2 = douban_url
    page_text = requests.get(url=url2, headers=headers).text
    tree2 = etree.HTML(page_text)
    douban_rating = tree2.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/strong/text()')
    if douban_rating != [] and douban_rating != ['  ']:
        douban_rating_list.append(eval(douban_rating[0]))

print("电影豆瓣平均分为：\n",sum(douban_rating_list)/len(douban_rating_list), end='')