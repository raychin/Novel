# coding: utf-8
import requests
#网页解析
from bs4 import BeautifulSoup
#正则表达式
import re

try:
    from common import proxy_utils
except ImportError:
    print('请在项目根目录中运行')
    exit(-1)

time_out = 10

def requestNovelChapter(req_url_base, txt_id, req_header):
    #proxies = proxy_utils.get_ip()
    txt = {}
    result = []
    txt['title'] = ''
    txt['id'] = str(txt_id)
    req_url = req_url_base + txt['id'] + '/'
    req_header['Referer'] = req_url
    print('header Referer >> ' + req_header['Referer'])
    try:
        print("小说首页地址>> " + req_url)
        r = requests.get(req_url, params = req_header, timeout = time_out)
        #r = requests.get(req_url, params = req_header, timeout = time_out, proxies = proxies)
        # soup转换
        soups = BeautifulSoup(r.text, "html.parser")
        if(len(soups.select('#wrapper .box_con #maininfo #info h1')) == 0):
            return txt, result;
        txt['title'] = soups.select('#wrapper .box_con #maininfo #info h1')[0].text          # 获取小说题目
        txt['author'] = soups.select('#wrapper .box_con #maininfo #info p')
        txt['update'] = txt['author'][2].text                                                       # 获取小说最近更新时间
        txt['lately'] = txt['author'][3].text                                                     # 获取最近更新章节名称
        txt['author'] = txt['author'][0].text                                                       # 获取小说作者
        txt['intro'] = soups.select('#wrapper .box_con #maininfo #intro')[0].text.strip()            # 获取小说简介
        print("编号：" + '{0:0>8}   '.format(txt['id']) + "小说名：《" + txt['title'] + "》  开始下载。" + txt['intro'] + txt['author'])
        pages = soups.select('#wrapper .box_con #list dl dd a')                          # 获取小说所有章节信息
        section_ct = len(pages)                                                                # 获取小说总章页面数
        for index in range(section_ct):
            split_str = pages[index]['href'].split('/')
            position = 0;
            if(len(split_str) > 1):
                position = len(split_str) - 1
            result.append(pages[index]['href'].split('/')[position])
        #first_page = pages[0]['href'].split('/')                           #获取小说第一章页面地址
    except(IOError, ConnectionError) as e:
        print('连接异常' + str(e))   
    return txt, result


# 获取小说内容
def requestNovelText(req_url, req_header):
    #proxies = proxy_utils.get_ip()
    print('小说下载地址>> ' + req_url)
    section_name = ''
    section_text = ''
    req_header['Referer'] = req_url
    print('header Referer >> ' + req_header['Referer'])
    try:
        # 请求当前章节页面  params为请求参数
        r = requests.get(req_url, params = req_header, timeout = time_out)
        #r = requests.get(req_url, params = req_header, timeout = time_out, proxies = proxies)
        # soup转换
        soup = BeautifulSoup(r.text, "html.parser")

        ''' 方式一，通过匹配获取
        # 获取章节名称              
        section_name = soup.find("div", class_ = "bookname").find("h1").text
        # 获取章节文本
        section_text = soup.find("div", id = "content")
        [s.extract() for s in section_text('script')]    #删除无用项
        '''

        #''' 方式二，通过标签层级获取
        # 获取章节名称
        print('文本地址 >> %s' % req_url)                 
        section_name = soup.select('#wrapper .content_read .box_con .bookname h1')[0].text
        # 获取章节文本
        section_text = soup.select('#wrapper .content_read .box_con #content')[0]
        for ss in section_text.select("script"):                #删除无用项
            ss.decompose()
        #'''

        # 按照指定格式替换章节内容，运用正则表达式
        section_text = re.sub( '\s+', '\r\n\t', section_text.text).strip('\r\n')
    except(IOError, ConnectionError) as e:
        print('连接异常' + str(e))      
    return section_name, section_text