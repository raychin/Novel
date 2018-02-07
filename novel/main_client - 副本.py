# coding: utf-8
import requests
#多线程
import threading
#网页解析
from bs4 import BeautifulSoup
#正则表达式
import re
#获取时间
import time

try:
    from common import file_utils
except ImportError:
    print('请在项目根目录中运行')
    exit(-1)

#请求头字典
req_header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'UM_distinctid=1609c270ce7563-0420093576ac3f-b7a103e-1fa400-1609c270ce8dcc; PTCMS_history=2%2C1',
    'Host':'m.biquge.in',
    'Referer':'http://www.biquge.in/b_2/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36',
}


req_url_base = 'http://www.qu.la/book/'           #小说主地址
req_url = req_url_base + "62416/"                 #单独一本小说地址
txt_section = '3267076.html'                      #某一章页面地址


def main():
    '''
    主函数
    '''
    # 创建下载文件夹
    file_utils.mkdir(file_utils.root_path)
    # 创建下载书籍存放文件夹
    file_utils.mkdir(file_utils.book_path)

    # 请求当前章节页面  params为请求参数
    r = requests.get(req_url + str(txt_section), params = req_header)
    # soup转换
    soup = BeautifulSoup(r.text, "html.parser")
    # 获取章节名称                                
    section_name = soup.find("div", class_="bookname").find("h1").text
    # 获取章节文本
    section_text = soup.find("div", id="content")
    [s.extract() for s in section_text('script')]    #删除无用项
    # 按照指定格式替换章节内容，运用正则表达式
    section_text = re.sub( '\s+', '\r\n\t', section_text.text).strip('\r\n')
    print('章节名:' + section_name)
    print('章节内容：\n' + section_text)
    if(file_utils.openSaveTxt(file_utils.book_path + "\\" + section_name + ".txt", section_text)):
        print('文本内容：\n' + file_utils.readTxt(file_utils.book_path + "\\" + section_name + ".txt"))

if __name__ == '__main__':
    main()