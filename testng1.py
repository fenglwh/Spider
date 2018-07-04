#!/usr/bin/python
# coding:utf-8
__Author__ = 'Adair.l'
import bs4
import urllib.request
content=urllib.request.urlopen("http://www.meizitu.com/a/5591.html").read().decode('gbk')
bs=bs4.BeautifulSoup(content,"lxml")
pics=[picture.attrs["src"] for picture in bs.find("div", id="picture").find_all("img")]