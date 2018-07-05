#!/usr/bin/python
# coding:utf-8
__Author__ = 'Adair.l'
import multiprocessing
import psutil
import os
import urllib.request
import bs4
import threadpool
class Spider():
    def __init__(self):
        self.store_path=''
        self.timeout=20
        self.thread_count=5
        self.process_count=8
        # self.process_count=psutil.cpu_count()

    def working(self):
        pass

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

    def retrieve_imgs(self,urls):
        print("retrieve imgs")
        tp=threadpool.ThreadPool(self.thread_count)
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
        pool=multiprocessing.Pool(processes=self.process_count)
        for url,store_path in url_and_paths:
            pool.apply_async(self.get_page,(url,store_path))
        pool.close()
        pool.join()
        print("pool joined")

if __name__ == '__main__':
    s=Spider()
    s.get_pages([("http://www.meizitu.com/a/{}.html".format(x),"mzt/{}".format(x)) for x in range(3525,6000)])


