#!/usr/bin/python
# coding:utf-8
__Author__ = 'Adair.l'
import multiprocessing
import threading
import psutil
import os
import urllib.request
import time
import bs4
import threadpool
class Spider():
    def __init__(self):
        self.store_path=''
        self.timeout=10
        self.thread_count=3

    def working(self):
        pass

    def retrieve(self,url,path):
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
                try:
                    os.remove(path)
                except:
                    pass
                print(e)
            else:
                print(e)

    def retrieve_imgs(self,urls):
        print("retrieve imgs")
        tp=threadpool.ThreadPool(5)
        for index,url in enumerate(urls):
            path= os.path.join(self.store_path,str(index)+".jpg" if len(os.path.splitext(url))>1 else os.path.splitext(url)[1])
            reqs=threadpool.makeRequests(self.retrieve,[((url,path),{})])
            for req in reqs:
                tp.putRequest(req)
        tp.wait()


    def get_page(self,url,store_path):
        print(url)
        self.store_path=store_path
        content = urllib.request.urlopen(url).read().decode('gbk')
        bs = bs4.BeautifulSoup(content, "lxml")
        pics = [picture.attrs["src"] for picture in bs.find("div", id="picture").find_all("img")]
        self.retrieve_imgs(pics)

    def get_pages(self,url_and_paths):
        pool=multiprocessing.Pool(processes=psutil.cpu_count()*4)
        for url,store_path in url_and_paths:
            pool.apply_async(self.get_page,(url,store_path))
        pool.close()
        pool.join()
        print("pool joined")

if __name__ == '__main__':
    s=Spider()
    s.get_pages([("http://www.meizitu.com/a/5591.html","mzt/1")])
    # s.store_path='mzt/1'
    # s.retrieve_imgs(['http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/01.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/02.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/03.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/04.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/05.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/06.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/07.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/08.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/09.jpg', 'http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/10.jpg'])