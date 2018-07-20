import requests
import bs4
import os
import urllib.parse
from http import cookiejar

class Spider:

    def __init__(self):
        self.store_path = ""
        self.page_index = 1
        self.img_index = 1

    def get_page(self, url):
        print("getting:{}".format(url))
        response=requests.get(url)
        print(response)
        bs = bs4.BeautifulSoup(response.text, "lxml")
        pics = [picture.attrs["data-src"] for picture in bs.find_all("img", attrs={"class": "load-src"})]
        try:
            os.makedirs(os.path.join(self.store_path, str(self.page_index)))
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
            print(response)
            path = os.path.join(self.store_path, str(self.page_index),str(self.img_index)) + ('.jpg' if response.headers[
                                                                                 'Content-Type'] == 'image/jpeg' else ".unknow")
            print(path)
            open(path, 'wb').write(response.content)
            self.img_index += 1
        self.page_index += 1
        self.img_index = 1
        next_page = [x for x in bs.select("html > body.white > div.view-paging > div.container > a.block") if x.text == '下一章'][
            0].attrs['href']
        if 'javascript:ShowEnd();' not in next_page:
            split_result = urllib.parse.urlsplit(url)
            split_result_list = list(split_result)
            split_result_list[2] = next_page
            self.get_page(urllib.parse.urlunsplit(split_result_list))


if __name__ == '__main__':
    s = Spider()
    s.store_path = "comic/绿茶婊气运师"
    s.page_index=1
    s.get_page(r"http://cnc.dm5.com/m575919/")
