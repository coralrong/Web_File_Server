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
#Reference:
#
#
#        WANG HAIPING (i_free001@njupt.edu.cn)
#
##########################################################
import html

XHTML_DOCTYPE_HEAD = '''<!DOCTYPE xhtml>\r\n<html>\r\n<head>\r\n
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">\r\n
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\r\n'''

class XHTML:
    'an XHTML generator' 

    # 初始化
    def __init__(self,doctype = True):
        self.xhtml         = ''
        self.finalized     = False
        if doctype:
            self.xhtml    += XHTML_DOCTYPE_HEAD

    # 检测tag是否有效
    def tag_checker(self,tag):
        assert len(tag) > 0 and tag[0] != '<' and tag[-1] != '>' \
            and (tag.lower() == tag or tag == '!DOCTYPE'),\
            f'{tag} is an invalid tag!'
        return self

    # 清空
    def cleanup(self,doctype = True):
        self.xhtml = ''
        self.finalized     = False
        if doctype:
            self.xhtml    += XHTML_DOCTYPE_HEAD
        return self

    #放入内容
    def extend(self,*raws):
        assert not self.finalized,'It has been finalized!'
        for s in raws:            
            if not self.xhtml:
                # If this is the first token,we'll strip off the left white chars if any
                self.xhtml += s.lstrip()
            else:
                self.xhtml += s
        return self

    # 结束tag
    def end_tag(self,tag):
        ''' add '</xxx>' tokens for this object'''
        self.tag_checker(tag)          
        return self.extend('</' + tag + '>\r\n')     

    # 开始tag
    def begin_tag(self,tag,dix = {},end_tag = False):   #地址问题不是这儿
        self.tag_checker(tag)
        s = '<' + tag
        if len(dix):
            for k,v in dix.items():
                s += ' ' + k + '="' + str(v)+ '"'
        if end_tag:
            s += '/'
        s += '>\r\n'
        return self.extend(s)


    def addtag(self,tag,inner,dix={}):
        ''' add a block tag with inner text/html'''
        return self.begin_tag(tag,dix,False).append(inner).end_tag(tag)

    def __add__(self,other):
        if isinstance(other,XHTML):
            return self.extend(other.finalize())
        assert isinstance(other,str),'other must be a string!'
        return self.extend(other)
    
    def append(self,x):
        self += x
        if not x.endswith('\n'):
            self += '\r\n'
        return self

    def inner_html(self,shtml):
        return self.append(shtml)

    def inner_text(self,stext):
        return self.append(stext)


    def load_file(self,file_path):
        ''' Load xhtml contents from a file. Mostly this file
        could be either a javascript file or a style file. Also,
        you can call this method to load a raw xhtml file!
        '''
        with open(file_path,"r",encoding='utf-8') as f:
            s = f.read()
            if s:
                self.append(s)
                loaded = True
        assert loaded,f"can't load {file_path} file!"
        return self

    # 加载CSS
    def load_style(self,style_file):
        return self.begin_tag('style').load_file(style_file).end_tag('style')

    # 加载javascript
    def load_script(self,script_file):
        return self.begin_tag("script").load_file(script_file).end_tag('script')

    # 构造完成
    def finalize(self):        
        self.finalized  = True
        return self.xhtml            

    
