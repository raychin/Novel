# coding: utf-8
import flask
from flask import request
from flask import jsonify

try:
    from user import login_server
except ImportError:
    print('请在项目根目录中运行')
    exit(-1)


VERSION = "1.1.1"

'''
flask： web框架，可以通过flask提供的装饰器@server.route()将普通函数转换为服务
登录接口，需要传url、username、passwd
'''
#创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)
#server.config['JSON_AS_ASCII'] = False

# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
@server.route('/user/login', methods=['get', 'post'])
def login():
    return jsonify(login_server.login(request))

if __name__ == '__main__':
    #指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
    server.run(debug=True, port=8888, host='0.0.0.0')