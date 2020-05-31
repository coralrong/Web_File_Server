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
from http import HTTPStatus
from utils import *
from local_server import *
import xhtml
import random
import string
from shutil import copyfile


os.chdir(os.path.dirname(os.path.abspath(__file__)))

class XFILE_HANDLER(UrlHandler):

    #加载一些CSS文件和基地址
    XFILE_CSS  = 'html/utils/main.css'
    AUTHENTICATE_CSS = 'html/utils/authenticate.css'
    XFILE_ROOT = '/disk/'



    #计算文件大小  转换为易读形式
    def calculate_size(self,size):
        fu=['B','KB','MB','GB']
        for index in range(4):
            if (size<1024):
                return str(round(size,2))+fu[index]
            else:
                size=size/1024


    #遍历当前文件夹
    def dir(self,file_path):
        all = os.listdir(file_path)
        x   = xhtml.XHTML(False)

        for a in all:
            #跳过存储用户信息的文件
            if (a=='admin.txt'):
                continue


            # 构造每一个文件专属块
            # 文件和文件夹的可操作性属性不同所以要单独处理

            x.begin_tag('div',dix={'class':'title'})
            url='http://127.0.0.1:7777/'+file_path+'/'+a
            fs_path=file_path+'/'+a

            # 文件夹
            if os.path.isdir(fs_path):
                fs_path=fs_path[5:]
                x.begin_tag('div',dix={'class':'biao4'})
                x.begin_tag('a',dix={'href':url})
                x.extend(fs_path.replace('\\','/')).end_tag('a').end_tag('div')

                x.begin_tag('div',dix={'class':'biao2'}).extend('Folder').end_tag('div')
                x.begin_tag('div',dix={'class':'biao3'})
                x.begin_tag('div',dix={'class':'but'}).extend('&nbsp').end_tag('div')
                x.begin_tag('div',dix={'class':'but'}).extend('&nbsp').end_tag('div')
                x.begin_tag('div',dix={'class':'but'})
                x.begin_tag('a',dix={'href':url}).extend('Open').end_tag('a').end_tag('div')
                x.end_tag('div').end_tag('div')

            # 文件
            else:
                size = os.path.getsize(fs_path)
                fs_path=fs_path[5:]

                x.begin_tag('div',dix={'class':'biao4'})
                x.begin_tag('a',dix={'href':url})
                x.extend(fs_path.replace('\\','/')).end_tag('a').end_tag('div')

                x.begin_tag('div',dix={'class':'biao2'}).extend(self.calculate_size(size)).end_tag('div')
                x.begin_tag('div',dix={'class':'biao3'})
                if (file_path.endswith('share')):
                    x.begin_tag('form',dix={'action':url+'/authenticate','method':'post'})
                    x.begin_tag('input',dix={'type':'text','class':'but','name':'secret'},end_tag=True)
                    x.begin_tag('div',dix={'class':'but'}).extend('&nbsp').end_tag('div')
                    x.begin_tag('input',dix={'type':'submit','value':'authenticate','class':'but'},end_tag=True)
                    x.end_tag('form').end_tag('div').end_tag('div')
                else:

                    x.begin_tag('div',dix={'class':'but'})
                    if (a.endswith('.jpg') or a.endswith('.png') ):      #添加预览标签
                        x.begin_tag('a',dix={'href':url}).extend('Preview').end_tag('a')
                    else:
                        x.extend('&nbsp')
                    x.end_tag('div')

                    x.begin_tag('div',dix={'class':'but'})
                    x.begin_tag('a',dix={'href':url+'/share'}).extend('Share').end_tag('a')
                    x.end_tag('div')


                    x.begin_tag('div',dix={'class':'but'})
                    x.begin_tag('a',dix={'href':url,'download':''}).extend('Download').end_tag('a').end_tag('div')
                    x.end_tag('div').end_tag('div')
        return x.finalize()

    def list_dir(self,file_path):

        #创建HTML对象
        x = xhtml.XHTML()

        #添加title
        x.begin_tag("title").extend(file_path).end_tag('title')
        x.load_style(self.XFILE_CSS)
        x.end_tag('head')
        x.begin_tag("body")

        #添加logo和用户
        x.begin_tag('div',dix={'class':'box'})
        x.begin_tag('div',dix={'class':'head'})
        x.extend('NPAN').end_tag('div')
        x.begin_tag('div',dix={'class':'count'})
        x.begin_tag('div',dix={'class':'profile'})
        x.begin_tag('img',dix={'src':'http://127.0.0.1:7777/html/image/B17040819.jpg'},end_tag=True)
        x.end_tag('div')
        x.begin_tag('div',dix={'class':'u'})
        name=file_path[5:14]
        x.extend(name).end_tag('div')
        x.end_tag('div').end_tag('div').end_tag('div')

        #添加bar
        x.begin_tag('div',dix={'class':'title'})
        x.begin_tag('div',dix={'class':'biao1'}).extend('Filename').end_tag('div')
        x.begin_tag('div',dix={'class':'biao2'}).extend('Size').end_tag('div')
        x.begin_tag('div',dix={'class':'biao3'}).extend('Action').end_tag('div')
        x.end_tag('div')

        #添加parent  和upload
        print()
        if (file_path[-1]=='/'):
            t = file_path[:-1]
        else:
            t=file_path

        if (file_path.count('/')==1):
            parent = 'http://127.0.0.1:7777/'+file_path
        else:
            parent= 'http://127.0.0.1:7777/'+file_path[0:file_path.rindex('/')]

        x.begin_tag('div',dix={'class':'title'})
        x.begin_tag('div',dix={'class':'biao4'})
        x.begin_tag('a',dix={'href':parent}).extend('Parent').end_tag('a')
        x.end_tag('div')
        x.begin_tag('div',dix={'class':'biao2'}).extend('Folder').end_tag('div')
        x.begin_tag('div',dix={'class':'biao3'})
        x.begin_tag('form',dix={'action':'http://127.0.0.1:7777/'+file_path,'method':'POST','name':'file_update','enctype':'multipart/form-data'})
        x.begin_tag('input',dix={'type':'file','name':'save_file'},end_tag=True)
        x.begin_tag('input',dix={'type':'submit','name':'sub','value':'Upload'},end_tag=True)
        x.end_tag('form').end_tag('div').end_tag('div')

        x.extend(self.dir(file_path))
        if (file_path.count('/')==1):
            share_path='disk/share'
            x.extend(self.dir(share_path))
        x.end_tag('body').end_tag('html')
        return x.finalize()


    #检测请求地址是否合规
    def check(self,path,req):
        if (path.startswith(XFILE_HANDLER.XFILE_ROOT) or path.startswith(XFILE_HANDLER.XFILE_ROOT[:-1]) or path.startswith('/html/image/')):

            if (path.endswith(XFILE_HANDLER.XFILE_ROOT) or path.endswith(XFILE_HANDLER.XFILE_ROOT[:-1])):
                print('permissions denied')
                return False
            else:
                return True
        return False


    def get_handler(self,path,req):
        fi=path[1:]
        if os.path.isdir(fi):   # 文件夹则遍历其中文件并展示
            req.msg_sender(HTTPStatus.OK,self.list_dir(fi))  
        else:                   # 是文件就打开直接发送
            if not os.path.exists(fi):
                print(f'[{fi}] is not existing!')
                req.msg_sender(HTTPStatus.NOT_FOUND,f'I\'m sorry, [{fi}] is not existing')                   
            else:
                req.file_sender(fi)
        return 

    def get_authenticate(self,path,req):   #共享方式
        #  将文件复制到共享文件夹
        source = path[1:-6]
        print('source: ' + source)
        name = source[source.rindex('/')+1:]
        print('name :' + name)
        target = 'disk/share/'+name
        print('target: '+ target)
        copyfile(source,target)

        #   随机生成10位字符和数字组成的密钥
        random_string= ''.join(random.sample(string.ascii_letters+string.digits,10))
        flag=False

        #更新或创建密钥信息
        with open('disk/share/admin.txt') as f:
            with open('disk/share/admin_new.txt','w+') as g:
                for line in f.readline():
                    if (line==''):
                        break
                    else:
                        file = line.split(' ')
                        if (file[0]==name):
                            continue
                        else:
                            g.write(line)
                s=name+' '+random_string+'\n'
                g.write(s)
        os.remove('disk/share/admin.txt')
        os.rename('disk/share/admin_new.txt','disk/share/admin.txt')

        #构建相应的HTML对象
        x = xhtml.XHTML()

        #添加title
        x.begin_tag('title').extend(path).end_tag('title')
        x.load_style(self.AUTHENTICATE_CSS)
        x.end_tag('head')
        x.begin_tag('body')
        x.begin_tag('div',dix={'id':'bo'})
        x.begin_tag('div').extend('Authenticate Code is :').end_tag('div')
        x.begin_tag('div').extend(random_string).end_tag('div')
        url = 'http://127.0.0.1:7777/'+source[:source.rindex('/')]
        x.begin_tag('a',dix={'href':url}).extend('OK').end_tag('a')
        x.end_tag('div')
        x.end_tag('body').end_tag('html')
        req.msg_sender(HTTPStatus.OK,x.finalize())

    def post_handler(self,path,data,req):
        raise RuntimeError('We have not supported POST verb so far!')

@main
def xfile():
    #
    # start the server here & now !
    #
    start([XFILE_HANDLER()])

