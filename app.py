# -*- coding=utf-8 -*-

@app.route('/')
def index():
    '''
    显示文章名称的列表
    页面中需要显示 ｀/home/shiyanlou/files/｀目录下所有的json文件
    中的｀title｀信息列表
    '''


@app.route('/files/<filename>')
def file(filename):
    '''
    读取并显示 filename.json中的文章内容
    例如 filename='helloshiyanlou'的时候显示helloshiyanlou.json
    中的内容
    如果filename不存在，则显示包含字符串｀shiyanlu 404｀ 404页面错误
    '''



