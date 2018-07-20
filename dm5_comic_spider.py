import requests
import bs4
import os
import urllib.parse
from http import cookiejar
import time
import datetime
import multiprocessing.pool

class Spider:

    def __init__(self):
        self.store_path = ""
        self.chapter_index = 1
        self.img_index = 1

    def get_chapter_default(self, url):
        print("getting:{}".format(url))
        response=requests.get(url)
        print(response)
        bs = bs4.BeautifulSoup(response.text, "lxml")
        pics = [picture.attrs["data-src"] for picture in bs.find_all("img", attrs={"class": "load-src"})]
        try:
            os.makedirs(os.path.join(self.store_path, str(self.chapter_index)))
        except:
            pass
        print("getting pics:{}".format(len(pics)))
        for pic in pics:
            headers = {
                'Host': urllib.parse.urlsplit(pic)[1],
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': url,
                'Connection': 'keep-alive',
            }
            print('getting:',pic)
            response = requests.get(pic,headers=headers)
            path = os.path.join(self.store_path, str(self.chapter_index), str(self.img_index)) + ('.jpg' if response.headers[
                                                                                 'Content-Type'] == 'image/jpeg' else ".unknow")
            open(path, 'wb').write(response.content)
            self.img_index += 1
        self.chapter_index += 1
        self.img_index = 1
        next_pages = [x for x in bs.select("html > body.white > div.view-paging > div.container > a.block") if x.text == '下一章']
        if next_pages:
            next_page=next_pages[0].attrs['href']
            if 'javascript:ShowEnd();' not in next_page:
                split_result = urllib.parse.urlsplit(url)
                split_result_list = list(split_result)
                split_result_list[2] = next_page
                self.get_chapter_default(urllib.parse.urlunsplit(split_result_list))

    def get_chapter_selenium(self,url):
        self.chapter_index = 1
        url = url
        pool = multiprocessing.pool.ThreadPool(processes=5)

        def get_imgs(imgs,chapter_path):#img,store path
            def get_img(img):
                for img_url,img_path in img:
                    headers = {
                        'Host': urllib.parse.urlsplit(img_url)[1],
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                        'Accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': url,
                        'Connection': 'keep-alive',
                    }
                    response = requests.get(img_url, headers=headers)
                    open(img_path, 'wb').write(response.content)

            img_index = 1
            for img in imgs:
                path=os.path.join(chapter_path,str(img_index)+'.jpg')
                pool.apply_async(img,path)
                img_index+=1

        def next_chapter():
            pass

        def next_page():
            pass

        def get_page(url):
            pass
        imgs=[]
        pool.close()
        if next_chapter():
            self.get_chapter_selenium(next_chapter())

if __name__ == '__main__':
    s = Spider()
    s.store_path = "comic/英雄我早就不当了"
    s.chapter_index=1
    s.get_chapter_default(r"http://www.1kkk.com/ch1-441730/")
