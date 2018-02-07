# coding: utf-8
import flask
from flask import request
 
def login(request):
    # 获取通过url请求传参的数据
    username = request.values.get('name')
    # 获取url请求传的密码，明文
    pwd = request.values.get('pwd')
    print('username = ' + username + ', pwd = ' + pwd)
    # 判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
    if username and pwd:
        # 执行sql，如果查询的username和password不为空，说明数据库存在admin的账号
        sql = 'select name,password from test where name= "%s" and password= "%s";' %(username, pwd)
        # 从数据查询结果后，res返回是元组
        res = '不为空'
        if res:  # res的结果不为空，说明找到了username=admin的用户，且password为加密前的123456
            resu = {'code': 200, 'message': '登录成功'}
            return resu # 将字典转换为json串, json是字符串
        else:
            resu = {'code': -1, 'message': '账号/密码错误'}
            return resu
    else:
        resu = {'code': 999, 'message': '必填参数未填写'}
        return resu