#!/usr/bin/python
# coding:utf-8
__Author__ = 'Adair.l'
import datetime
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.common.keys as keys
import selenium.common
import time
import urllib.request
import os
import threading


class Spider():
    def __init__(self):
        self.retrieve_path = os.path.dirname(__file__)
        self.driver = None
        self.thread_no = 5
        self.timeout = 10
        self.store_path="debug/"

    def load_driver(self, type="phantomjs"):
        print("loading driver")
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        self.driver = selenium.webdriver.Chrome(executable_path=r'C:\Users\fengl\Desktop\tools\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)
        self.driver.set_window_size(1920, 1080)
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)
        print("driver loaded")

    def quit_driver(self):
        self.driver.quit()

    def work(self, url):
        print("getting url: {}".format(url))
        url_base = os.path.dirname(url)
        try:
            self.driver.get(url)
        except selenium.common.exceptions.TimeoutException as e:
            try:
                print("Fail to get url, retring...")
                self.driver.get(url)
            except:
                print("{} fail get\n".format(url))
                open("log", 'a').write("{} fail get\n".format(url))
                return

        print("wait for load")
        time_start=datetime.datetime.now()
        while (datetime.datetime.now()-time_start).total_seconds()<500:
            items = self.driver.find_elements_by_xpath("/html/body/div[@id = 'mainView']/ul/li/img")
            try:
                for index, item in enumerate(items):
                    if item.get_attribute("class") != 'loaded':
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_UP)
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_UP)
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_DOWN)
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_DOWN)
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_DOWN)
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_DOWN)
                        self.driver.find_element_by_xpath("/html/body").send_keys(keys.Keys.PAGE_DOWN)
                        print('pic index: {}/{} not loaded, this is the {}th time'.format(index, len(items), index))
                        time.sleep(0.1)
                        break
                else:
                    break
            except Exception as e:
                print(e)
                break
        items = self.driver.find_elements_by_xpath("/html/body/div[@id = 'mainView']/ul/li/img")

        urls = [item.get_attribute("src") for item in items]
        threading.Thread(target=self.get_items, args=(urls,),
                         kwargs={"store_path": "{}/{}".format(self.store_path, url.replace(url_base + '/', ''))}).start()

    def get_items(self, urls, store_path):
        def get_item(url, file_no=0):
            print("retrieveing {}/{}".format(file_no, len(urls)))
            for x in range(3):
                header = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:53.0) Gecko/20100101 Firefox/53.0", }
                req = urllib.request.Request(url, headers=header)
                file_path = os.path.join(self.retrieve_path, "{}/{}.jpg".format(store_path, file_no))
                if not os.path.exists(os.path.dirname(file_path)):
                    try:
                        os.makedirs(os.path.dirname(file_path))
                    except:
                        pass
                try:
                    open(file_path, 'wb').write(urllib.request.urlopen(req, timeout=self.timeout).read())
                    break
                except Exception as e:
                    if "timeout" in str(e).lower():
                        print(e)
                    else:
                        print(e)
            else:
                open("log.txt", 'a').write("{} not downloaded".format(url))
        # actually this part should use pool instead, but I am a lazy guy
        threads = [threading.Thread(target=get_item, args=(x, index)) for index, x in enumerate(urls)]
        for i in range(self.thread_no if len(threads) > 5 else len(threads)):
            threads[i].start()

        while threads:
            dead = []
            for i in range(self.thread_no if len(threads) > 5 else len(threads)):
                if not threads[i].is_alive():
                    dead.append(i)
            for i in dead[::-1]:
                threads.pop(i)
            for i in range(self.thread_no - len(dead), self.thread_no if len(threads) > 5 else len(threads)):
                threads[i].start()
            print("remain {} retrieve thread running".format(len(threads)))
            time.sleep(0.1)

    def get_pages(self, url_list):
        self.load_driver()
        for url in url_list:
            self.work(url)
        self.quit_driver()

    def get_page(self, url):
        self.load_driver()
        self.work(url)
        self.quit_driver()


if __name__ == '__main__':
    s = Spider()
    s.store_path="comic/论恐女政的恋爱方法"
    s.get_pages(["http://ac.qq.com/ComicView/index/id/623291/cid/{}".format(x) for x in range(7, 62)])
