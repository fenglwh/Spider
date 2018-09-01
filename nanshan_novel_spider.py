import requests
import bs4
import urllib.parse
import os
import threadpool
import urllib.request
import multiprocessing

import time


class Spider():
    def __init__(self,index_page,path='/novel/grapped'):
        self.url=index_page
        self.store_path = path
        self.timeout = 20
        self.thread_count = 1
        self.process_count = 1
        self.seperate_time=1
        a = requests.get(index_page)
        # a = requests.get('https://www.szyangxiao.com/208952.shtml')
        self.host= urllib.parse.urlsplit(index_page)
        bs = bs4.BeautifulSoup(a.content, 'lxml')
        self.chapters = [(self.host.scheme+'://'+self.host.netloc+ x.attrs['href'],os.path.join(self.store_path,str(index)+x.text+'.txt')) for index,x in
                    enumerate(bs.select("html > body > div.wrapper > ul.nav.clearfix > span > a"))]


    def retrieve(self,url,path,retried=0):
        print("retrieve:",url)
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:53.0) Gecko/20100101 Firefox/53.0", }
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass
        try:
            req=urllib.request.Request(url,headers=header)
            open(path, 'wb').write(urllib.request.urlopen(req, timeout=self.timeout).read())
        except Exception as e:
            if "timeout" in str(e).lower():
                print(e)
            else:
                print(e)
            try:
                os.remove(path)
            except:
                pass
            if not retried:
                self.retrieve(url,path,1)



    def get_page(self,url,store_path):
        print(url)
        content = requests.get(url).content.decode('gbk')
        bs = bs4.BeautifulSoup(content, "lxml")
        page = ''.join([page.text for page in  bs.select("html > body > div > p")])
        if not page:
            print(store_path)
            print(content)
        try:
            os.makedirs(os.path.dirname(store_path))
        except Exception as e:
            pass
        open(store_path,'wb').write(page.encode('utf-8'))

    def get_pages(self,url_and_paths):
        pool=multiprocessing.Pool(processes=self.process_count)
        for url,store_path in url_and_paths:
            pool.apply_async(self.get_page,(url,store_path))
            time.sleep(self.seperate_time)
        pool.close()
        pool.join()
        print("pool joined")
if __name__ == '__main__':
    s=Spider('https://www.szyangxiao.com/208952.shtml','novel/娱乐超级奶爸')
    s.get_pages(s.chapters)
    # print(s.chapters)
    # s.get_page('https://www.szyangxiao.com/208952/zhangjie187811859.shtml', 'novel/娱乐超级奶爸\\第二百八十七章 强大的伴郎团.txt')