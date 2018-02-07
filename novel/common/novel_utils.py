# coding: utf-8
import requests
#网页解析
from bs4 import BeautifulSoup
#正则表达式
import re


# 获取小说内容
def requestNovelText(req_url, req_header):
    # 请求当前章节页面  params为请求参数
    r = requests.get(req_url, params = req_header)
    # soup转换
    soup = BeautifulSoup(r.text, "html.parser")
    # 获取章节名称                                
    section_name = soup.find("div", class_="bookname").find("h1").text
    # 获取章节文本
    section_text = soup.find("div", id="content")
    [s.extract() for s in section_text('script')]    #删除无用项
    # 按照指定格式替换章节内容，运用正则表达式
    section_text = re.sub( '\s+', '\r\n\t', section_text.text).strip('\r\n')
    #print('章节名:' + section_name)
    #print('章节内容：\n' + section_text)
    return section_name, section_text