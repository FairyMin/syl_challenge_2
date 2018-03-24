# -*- coding=utf-8 -*-
from flask import Flask
from flask import render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/mydb'
db=SQLAlchemy(app)

#读取文件中的文件名
path = '/home/shiyanlou/files'
files = os.listdir(path)

#首页视图函数
@app.route('/')
def index():
    '''
    显示文章名称的列表
    页面中需要显示 ｀/home/shiyanlou/files/｀目录下所有的json文件
    中的｀title｀信息列表
    '''
    titles=[]   #存储每个文件的title
    #读取每个文件的内容，并存下title
    for file in files:
        with open(path+'/'+file,'r') as f:
            json_info = json.load(f)
            titles.append(json_info['title'])
    #返回模板并渲染
    return render_template('index.html',title_mod=titles)

#files页视图函数
@app.route('/files/<filename>')
def file(filename):
    '''
    读取并显示 filename.json中的文章内容
    例如 filename='helloshiyanlou'的时候显示helloshiyanlou.json
    中的内容
    如果filename不存在，则显示包含字符串｀shiyanlu 404｀ 404页面错误
    '''
    filename_j = filename+'.json'
    file_locate = path+'/'+filename+'.json'
    #判断文件是否存则，否则报404
    if filename_j not in files:
        abort(404)
    else:
        #文件存在，读取json
        with open(file_locate,'r') as f:
            file_info_dic = json.load(f)
#        file_info_list = []
#        for k,v in file_info_dic.items():
#            file_info_list.append((k,v))   
    #返回模板并渲染
    return render_template('file.html',file_info_mod=file_info_dic)

#404视图函数
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


#文章表，类别表的关系是 '多对一' 的关系，即一个类别有多篇文章

#数据表 File类－－对应－－文章表
class File(db.Model):
    #主键
    id = db.Column(db.Integer,primary_key=True)
    #文章标题
    title = db.Column(db.String(80))
    #文章创建时间
    created_time = db.Column(db.DateTime)
    #文章分类，外键约束
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('files',
                lazy='dynamic'))
    #文章内容
    content = db.Column(db.Text)

    def __init__(self,title,category,content,created_time=None):
        self.title = title
        
        if created_time is None:
            created_time = datetime.now()
        self.created_time = created_time

        self.category = category
        self.content = content


    def __repr__(self):
        return '<File %s>'%self.title


#数据表 Category类－－对应－－类别表
class Category(db.Model):
    #主键id
    id = db.Column(db.Integer,primary_key=True)
    #类别名称
    name = db.Column(db.String(80))
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %s>'%self.name


if __name__=="__main__":
    app.run()

