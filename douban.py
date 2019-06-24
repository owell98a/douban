from urllib import request
from bs4 import BeautifulSoup
import csv

class movie_datas:
    def __init__(self,url):
        self.page_url = [url]
        self.f_url = []
        self.grep = ['电影', '导演', '编剧', '主演', '类型', '语言', '上映日期', '片长', '又名']
        self.datas=[]

    # 把网页内容解析到BeautifulSoup可读
    def get_html(self,url):
        req = request.urlopen(url)
        html = req.read().decode('utf-8')
        content = BeautifulSoup(html, 'html5lib')
        return content

    # 获取每页的url
    def get_page(self,url):
        for i in range(1, 10):
            S = url + '?start=' + str(i * 25) + '&filter='
            self.page_url.append(S)
        return self.page_url

    # 获取每页中的电影跳转到主页面url, 返回list格式
    def get_movie(self,content):
        #content = self.get_html(url)
        movie_url = content.findAll('div', class_="item")
        #print(movie_url)
        for i in movie_url:
            film_url = i.a
            film_url = film_url.get('href')
            self.f_url.append(film_url)
        return self.f_url

    # 电影主界面解析,最终按照grep=['电影','导演','编剧','主演','类型','语言','上映日期','片长','又名'] 获取字段数据
    def movie_data(self,content):
        #content = self.get_html(url)
        fname = content.find('div', id='content')
        fname = fname.find('span', property="v:itemreviewed")
        fname = fname.text
        fdata = content.find('div', id='info').text
        fdata = fdata.split('\n')
        tmp = [i.strip() for i in fdata if len(i)]
        tmp_dict = {'电影': fname}
        # print (tmp)
        for i in tmp:
            i = i.split(':', 1)
            if len(i) >= 2:
                tmp_dict[i[0]] = i[1]
            # tmp_dict.append(i)
        #grep = ['电影', '导演', '编剧', '主演', '类型', '语言', '上映日期', '片长', '又名']
        fin_data = [tmp_dict[i] for i in self.grep]
        return fin_data
#存储
    def save_datas(self,fin_data):
        with open('./test.csv','w') as f:
            fcsv = csv.writer(f)
            fcsv.writerows(fin_data)

#开始
    def start(self,url):
        self.datas.append(self.grep)
        tmp=self.get_page(url)  #获取各页链接，返回list
        for i in tmp:
            tmp1=self.get_html(i)  #返回html5lib格式文本
            tmp2=self.get_movie(tmp1) #返回页面上的各电影链接 list
            for i in tmp2:
                tmp3=self.get_html(i)
                tmp4=self.movie_data(tmp3) #返回电影对应的信息 list
                self.datas.append(tmp4)
        self.save_datas(self.datas)



if __name__=='__main__':
    url='https://movie.douban.com/top250'
    t=movie_datas(url)
    t.start(url)


