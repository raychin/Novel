# coding: utf-8
# 多线程
import threading
# 获取时间
import time

try:
    from common import file_utils
    from common import novel_utils
except ImportError:
    print('请在项目根目录中运行')
    exit(-1)

# 请求头字典
req_header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'UM_distinctid=1609c270ce7563-0420093576ac3f-b7a103e-1fa400-1609c270ce8dcc; PTCMS_history=2%2C1',
    'Host':'m.biquge.in',
    'Referer':'https://www.qu.la/book/16431/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36',
}


req_url_base = 'http://www.qu.la/book/'           # 小说主地址
req_url = req_url_base + "62416/"                 # 单独一本小说地址
txt_section = '3267076.html'                      # 某一章页面地址


def getNovel(novel_url, path, header):
    section_name, section_text = novel_utils.requestNovelText(novel_url, req_header)
    txt_path = path + "\\" + section_name + ".txt"
    if(file_utils.openSaveTxt(txt_path, section_name, section_text)):
        #print('文本内容：\n' + txt_path))
        print('保存成功')
    else:
        print('保存失败')


def getNovelByChapter(txt_id, chapter, path, header):
    novel_url = req_url_base + txt_id + '/' + chapter
    section_name, section_text = novel_utils.requestNovelText(novel_url, req_header)
    txt_path = path + "\\" + chapter.strip('.html') + ".txt"
    print(chapter)
    if(file_utils.isExistFile(txt_path) == False):
        if(file_utils.openSaveTxt(txt_path, section_name, section_text)):
            #print('文本内容：\n' + txt_path))
            print('保存成功')
        else:
            print('保存失败')
    else:
        print('已存在该文件')


def getNovels(novel_url, txt_id, header):
    txt, chapters = novel_utils.requestNovelChapter(novel_url, txt_id, header)
    txt_path = file_utils.book_path + txt_id + "\\"
    file_utils.mkdir(txt_path)

    '''
    # 测试代码
    thread_new = threading.Thread(target = getNovelByChapter, args = ('16431', '10558237.html', txt_path, req_header, ))
    thread_new.start()
    '''

    print('共有章节 >> %d' % len(chapters))
    for index in range(len(chapters)):
        print(req_url_base + txt_id + '/' + chapters[index])
        try:
            thread_new = threading.Thread(target = getNovelByChapter, args = (txt_id, chapters[index], txt_path, req_header, ))
            thread_new.start()
        except:
           print("Error: unable to start thread")
    

def main():
    '''
    主函数
    '''
    
    # 创建下载文件夹
    file_utils.mkdir(file_utils.root_path)
    # 创建下载书籍存放文件夹
    file_utils.mkdir(file_utils.book_path)

    # 创建线程，获取小说章节目录后再获取内容
    try:
        t1 = threading.Thread(target = getNovels, args = (req_url_base, '16431', req_header, ))
        t1.start()
    except:
       print("Error: unable to start thread")
    
    '''
    print('开启线程')
    # 创建线程获取小说内容
    try:
        t1 = threading.Thread(target = getNovel, args = (req_url + str(txt_section), file_utils.book_path + "\\", req_header, ))
        t1.start()
    except:
       print("Error: unable to start thread")
    print('线程完成')
    '''

    '''
    # 获取小说内容
    section_name, section_text = novel_utils.requestNovelText(req_url + str(txt_section), req_header)
    if(file_utils.openSaveTxt(file_utils.book_path + "\\" + section_name + ".txt", section_name, section_text)):
        print('文本内容：\n' + file_utils.readTxt(file_utils.book_path + "\\" + section_name + ".txt"))
    else:
        print('保存失败')
    '''

if __name__ == '__main__':
    main()