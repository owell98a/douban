from urllib import request
from bs4 import BeautifulSoup
import os
import csv

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

#电影主界面解析,最终按照grep=['电影','导演','编剧','主演','类型','语言','上映日期','片长','又名'] 获取字段数据
def movie_data(url):
    content=get_html(url)
    fname=content.find('div',id='content')
    fname=fname.find('span',property="v:itemreviewed")
    fname=fname.text
    fdata=content.find('div',id='info').text
    fdata=fdata.split('\n')
    tmp=[i.strip() for i in fdata if len(i)]
    tmp_dict={'电影':fname}
    #print (tmp)
    for i in tmp:
        i=i.split(':',1)
        if len(i)>=2:
            tmp_dict[i[0]]=i[1]
        #tmp_dict.append(i)

    grep=['电影','导演','编剧','主演','类型','语言','上映日期','片长','又名']
    fin_data=[tmp_dict[i] for i in grep]
    return fin_data

def save_data(test):
    with open('./test.csv','w') as f:
        fcsv=csv.writer(f)
        fcsv.writerow(test)



print (movie_data('https://movie.douban.com/subject/1292052/'))
t=movie_data('https://movie.douban.com/subject/1292052/')
save_data(t)









