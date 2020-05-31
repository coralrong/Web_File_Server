###############################################################
# 
# Module:
#
#        utils.py
#
# Author:
#
#        Coral_Rong(b17040819@njupt.edu.cn)
#
# Reference:
#
#
#       WANG HAIPING (i_free001@njupt.edu.cn)
#
##########################################################

# -*- coding: utf-8 -*-
import os
import re
from http import server
import io
import json
import socketserver
import subprocess
import sys
import urllib
import sys
import shutil
import urllib.parse
import webbrowser
import threading
import hashlib
import socket
from http import HTTPStatus
import mimetypes

from utils import *

SERVER_PORT = 7777

url_handlers = []

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def mime_detector(url):             #返回文件类型
    p = mimetypes.guess_type(url)
    if not p:
        p = 'application/octet-stream'
    else:
        p = p[0]
    return p
    
class UrlHandler:   #报错信息

    def check(self,path,req):
        raise RuntimeError('You must implement check in UrlHandler')
    
    def get_handler(self,path,req):
        raise RuntimeError('You must implement get_handler in UrlHandler')

    def post_handler(self,path,data,req):
        raise RuntimeError('You must implement post_handler in UrlHandler')
        

def getPassword(s):     #获取表单账户，密码信息
    n=s.find('&')
    username=s[9:n]
    password=s[n+10:]
    return username,password

def getSecret(s):       #获取认证密码
    return s[7:]

def url_to_filepath(s):         # /disk/share/t.txt/authenticate -> t.txt   地址转换
    s=s[12:-13]
    return s


#创建一个类，同时继承server和MixIn类就可以自动获得多线程并发处理能力
class ThreadedHTTPServer(socketserver.ThreadingMixIn, server.HTTPServer):
    #
    # override it here for we're a daemon thread
    #
    daemon_threads = True


class Handler(server.BaseHTTPRequestHandler):

    #检测请求地址是否合规，防止访问未授权信息造成信息泄露
    def check_handler(self,path):
     #   print('check_handler')
        for p in url_handlers:
            if p.check(path,self):
                return p
        return None




    def do_POST(self):
        print('do-POST')
        # 由于文件上传的表单数据过大，无法编码在url中，所以使用multipart/form-data
        # 因此可以根据content-Type区分POST请求的目的

        if (self.headers['Content-Type'] == 'application/x-www-form-urlencoded'):
            path = urllib.parse.unquote(self.path).lower()

            #构建了认证的请求url为 "主机+文件相对地址+authenticate"
            if (path.endswith('authenticate')):                         #共享文件认证
                datas = self.rfile.read(int(self.headers['content-length']))
                datas = datas.decode('utf-8')
                secret=getSecret(datas)     #获取表单附带的认证密钥
                print(path)
                filepath = url_to_filepath(path)        # /disk/share/t.txt/authenticate -> t.txt  提取文件名
                print(filepath)

                with open('disk/share/admin.txt') as f:     #查看共享文件密钥信息
                    while True:
                        it = f.readline()
                        if (it==''):
                            break;
                        else:
                            file = it.split(' ')
                            st_secret=file[1].strip('\n')
                            if (file[0]==filepath and st_secret==secret):   #用户名和密钥认证成功即发送文件
                                self.file_sender(path[1:-13])
                #出错返回提示html
                f=open('html/response.html',encoding='UTF-8')
                response=f.read()
                self.msg_sender(HTTPStatus.OK,response)
            else:
                #身份验证
                print()
                datas = self.rfile.read(int(self.headers['content-length']))    #读取附加字段信息
                datas=datas.decode('utf-8')
                print(datas)
                username,password=getPassword(datas)    #解码账户名密码
                admin_path='disk/'+username+'/admin.txt'

                with open(admin_path) as f:     #判断账户密码是否正确
                    st=f.read().split(' ')
                    r=hashlib.md5(password.encode('utf-8'))
                    if (st[1]==r.hexdigest()):
                        path='/disk/'+username
                        self.do_GET(True,path)  #正确返回相应用户主页
                    else:
                        f=open('response.html',encoding='UTF-8')
                        response=f.read()
                        self.msg_sender(HTTPStatus.OK,response)

        else:       #文件上传
            flag=False
            #提取文件名
            data=self.rfile.readline()
            data=self.rfile.readline()
            data=data.decode('utf-8').split(';')
            data=data[2]
            filename=data=data[11:-3]
            print(filename)
            path = urllib.parse.unquote(self.path).lower()
            filename=path[1:]+'/'+filename
            filename=filename.lower()
            self.rfile.readline()
            self.rfile.readline()

            #存入当前目录下
            with open(filename,'wb+') as f:
                while True:
                    data=self.rfile.readline()
                    s='------WebKitFormBoundary'
                    s=bytes(s,encoding='utf-8')
                    if (data.startswith(s)):
                            break;
                    else:
                        f.write(data)
                self.do_GET(True, path)     #更新上传成功后的网页







    #接收处理所有的“GET”请求
    def do_GET(self,flag=False,path='/'):
        print('do_GET')

        # 程序自定义的网页跳转和用户请求的网页，两种地址处理方式不同
        if (flag):
            path=path
        else:
            path = urllib.parse.unquote(self.path).lower()

        #请求根目录 则将登陆窗口发送
        if (path=='/'):
            f=open('html/login.html',encoding='UTF-8')
            response=f.read()
            self.msg_sender(HTTPStatus.OK,response)
        else:
            #请求共享文件夹文件
            if (path.endswith('share')):
                p    =self.check_handler(path)
                if p:
                    try:
                        return p.get_authenticate(path,self)    #执行密码认证
                    except Exception as e:
                        raise
                        print(e)
                        return
            else:
            #请求所登陆账号的文件
                p    = self.check_handler(path)
                print(path)
                if (p != None):
                    print("correct")
                if p:
                    try:
                        return p.get_handler(path,self)     #处理请求句柄
                    except Exception as e:
                        raise
                        print(e)
                        return
                notfound = "I'm sorry, nothong for you, baby!"
                self.msg_sender(HTTPStatus.NOT_FOUND,notfound)



    def file_sender(self,file_path,headers = {}):
        print('file_sender')

        # 查看文件类型等信息，进而构造回复的头
        mime_type = mime_detector(file_path)
        status    = HTTPStatus.OK
        try:
            size = os.path.getsize(file_path)
        except:
            size      = 0
            status    = HTTPStatus.NOT_FOUND
            mime_type = 'text/html'
        self.send_response(status)
        if 'Content-Type' not in headers:
            self.send_header('Content-Type',mime_type)
        self.send_header('Content-Length',size)
        for k,v in headers.items():
            print(k)
            print(v)
            self.send_header(k,v)
        self.end_headers()

        #将文件以二进制形式发送，调用socketserver封装好的wfile
        if size:
            with open(file_path,"rb") as f:
                while True:
                    b = f.read(1024*64)
                    if not b:
                        break
                    if not self.wfile.write(b):
                        break
        return 


    def msg_sender(self,status,msg, mime_type = 'text/html; charset=utf-8', headers = {}):
        print('msg_sender')
        self.send_response(status)  #发送状态码

        #构造回复头
        mtype = mime_type
        bmsg  = bytes(msg,'utf-8')
        if 'Content-Type' not in headers:
            if mtype and msg and 'charset' not in mtype:
                mtype += "; charset=utf-8"
            if mtype:
                self.send_header("Content-Type",mtype)

        self.send_header("Content-Length",str(len(bmsg)))
        for k,v in headers.items():
            self.send_header(k,v)
        self.end_headers()
        #调用wfile发送负载信息
        if msg:
            self.wfile.write(bmsg)

    def log_message(self, *args, **kwargs):
        print('log_message')
        pass
    

def start(handlers,port = 0,openbrowser = True):
    # 创建服务器端的套接字
    if port:
        global SERVER_PORT
        SERVER_PORT = port
    for h in handlers:
        url_handlers.append(h)

    url = f"http://0.0.0.0:{SERVER_PORT}"
    socketserver.TCPServer.allow_reuse_address = True   #允许复用套接字  因为多次访问后结束套接字，但是操作系统不会立即结束
    try:
        httpd = ThreadedHTTPServer(("0.0.0.0", SERVER_PORT), Handler)       #多线程TCP服务
    except OSError:       
        print(f"Port {SERVER_PORT} is already in use, likely for another instance of the server.")
        print("To open a second instance of the server, specify a different port using --port.")
        return
    
    print(f'\nStart Server listening on [{SERVER_PORT}]!')

    if openbrowser:
        webbrowser.open(f'http://127.0.0.1:{SERVER_PORT}', new=0, autoraise=True)    #此处打开就是发出第一个请求
    try:
        httpd.serve_forever()   #保持连接，即守护进程
    except KeyboardInterrupt:
        print(" - Ctrl+C pressed")
        print("Shutting down server - all unsaved work may be lost")
        print(
'''
      _____   _______    ____    _____  
     / ____| |__   __|  / __ \  |  __ \ 
    | (___      | |    | |  | | | |__) |
     \___ \     | |    | |  | | |  ___/ 
     ____) |    | |    | |__| | | |     
    |_____/     |_|     \____/  |_|     
''')
