#-*- coding:utf-8 -*-


import shutil
from flask import Flask, flash, request, redirect, url_for,render_template
import os
from werkzeug.utils import secure_filename

path="F:\\Upload"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','iso'])
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/aaa', methods=['GET', 'POST'])
def aaa():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        froms=request.form
        filename = froms['filename']
        no = froms['no']
        shardCount =int(froms['shardCount'])
        name =os.path.splitext(filename)[0]
        uploaded_files = request.files.getlist("file")  # 获取文件流集
        #先保存本地,方面本地读取
        for file in  uploaded_files:  # 这里改动以存储多份文件
            #保存流文件
            streamName = name+str(no)
            file.save(os.path.join(path, streamName))
        if (int(no))==(shardCount-1):        #如果读取完了就合并
            print('我在合并数据')
            mergeFile(filename,shardCount);  # 合并文件,合并后获取列表
            file_list = get_list()
            return render_template('success.html', file_list=file_list);



@app.route('/', methods=['GET'])
def get_list():
    file_list=get_list()
    return render_template('index.html', file_list=file_list);

def get_list():
    file_list=[]
    files=os.listdir(path)
    if len(files)>0:
        for file in files:
            Dir=os.path.join(path,file)
            if os.path.isdir(Dir):
                type='folder'
            else:
                type = "file"
            size = os.path.getsize(Dir)
            file_list.append({'name':file,'size':size,'url':Dir,'type':type})
    return file_list
#合并文件
def mergeFile(nm,shardCount):
    temp = open(path+"/"+nm,'wb')#创建新文件
    print('我来合并数据了')
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, "static\images", nm)
    the_file=os.path.splitext(nm)
    for i in range(0,shardCount):
        streamPath=os.path.join(path, the_file[0]+str(i))
        fp = open(streamPath, 'rb')  # 以二进制读取分割文件
        temp.write(fp.read())#写入读取数据
        fp.close()
        os.remove(streamPath)
    #把已经上传到本地的图片保存到本地方便前端读取（服务器不需要，可以直接通过http地址直接读取，不必在意）
    if  the_file[1]=='.jpg'or the_file[1]=='.png':
        shutil.copyfile(path+"/"+nm,upload_path)
    temp.close()

@app.route('/delete',methods=['POST'])
def delete():
    name = request.form['name']
    url=os.path.join(path,name)
    if os.path.exists(url):
        if os.path.isdir(url):
            os.rmdir(url)
        else:
            os.remove(url)
    file_list = get_list()
    return render_template('success.html',file_list=file_list);

if __name__ == '__main__':
    app.run(debug=True)
