# coding: utf-8
# 引入模块
import os
import sys


py_path = sys.path[0]
father_path = os.path.abspath(os.path.dirname(py_path) + os.path.sep + ".")


# 定义要创建的目录
root_path = father_path + "\\download_novel";        #下载目录
book_path = root_path + "\\book\\";                  #下载存放书籍目录

# 创建文件夹
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path, 0o777) 
 
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False



# 创建并保存内容到文件
def openSaveTxt(path, title, text):
    flag = False
    try:
        fo = open(path, "w")
        fo.write(title.encode('UTF-8'))
        fo.write('\n')
        fo.write(text.encode('UTF-8'))
        flag = True
    except IOError:
        print(path + ' 文件打开失败')
        flag = False
    fo.close()
    return flag

# 查询文件是否存在
def isExistFile(file_path):
    flag = False
    try:
        flag = os.path.exists(file_path)
    except IOError:
        print(file_path + ' 文件查询失败')
        flag = False
    return flag



# 读取指定目录文件内容
def readTxt(path):
    try:
        fo = open(path, "r")
        str = fo.read()
    except IOError:
        print(path + ' 文件打开失败')
    fo.close()
    return str