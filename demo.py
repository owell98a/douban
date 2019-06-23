from urllib import request
from bs4 import BeautifulSoup


url='https://movie.douban.com/top250'

#把网页内容解析到BeautifulSoup可读
def get_html(url):
    req=request.urlopen(url)
    html=req.read().decode('utf-8')
    content=BeautifulSoup(html,'html5lib')
    return content

#获取每页的url
page_url=[url]
def get_page(url):
    for i in  range(1,10):
        S = url + '?start=' + str(i * 25) + '&filter='
        page_url.append(S)
    return page_url

#获取每页中的电影跳转到主页面url, 返回list格式
f_url=[]
def get_movie(url):
    content=get_html(url)
    movie_url=content.findAll('div',class_="item")
    print (movie_url)
    for i in movie_url:
        film_url = i.a
        film_url = film_url.get('href')
        f_url.append(film_url)
    return f_url

print (get_movie(url))







