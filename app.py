from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////erolibrary.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class ImageInformation(db.Model):
    __tablename__ = "image_information"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_name = db.Column(db.String(80), unique=True)
    path_name = db.Column(db.String(120))
    ero = db.Column(db.Integer)
    bare = db.Column(db.Integer)
    hentai = db.Column(db.Integer)
    handsome = db.Column(db.Integer)
    sex = db.Column(db.Integer)

    def __init__(self, img_name, path_name, ero, bare, hentai, handsome, sex):
        self.img_name = img_name
        self.path_name = path_name
        self.ero = ero
        self.bare = bare
        self.hentai = hentai
        self.handsome = handsome
        self.sex = sex

    def __repr__(self):
        return '<img_name %r>' % self.img_name


db.create_all()  # 创建表


@app.route('/')
def index():
    img_list = ImageInformation.query.all()
    img_stream = return_img_stream(os.path.join(img_list[0].path_name, img_list[0].img_name))
    return render_template("index.html", img_list=img_list, img_stream=img_stream)


@app.route('/ajax_img', methods=['GET', 'POST'])
def ajax_img():
    info_img_name = request.form.get('IMG_NAME')
    info_img_path = request.form.get('IMG_PATH')
    new_img = str(info_img_path) + os.path.sep + str(info_img_name)
    print(new_img)
    new_img_json = {'data': "data:;base64," + return_img_stream(new_img)}
    return new_img_json


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
