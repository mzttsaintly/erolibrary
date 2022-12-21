import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

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
    img_list = ImageInformation.query.paginate(page=1, per_page=20, error_out=False)
    img_stream = return_img_stream("static/img/2021-02-25_01.jpg")
    return render_template("app.html", img_list=img_list.items, img_stream=img_stream)


@app.route('/getPic', methods=['GET', 'POST'])
def ajax_img():
    info_img_name = request.form.get('IMG_NAME')
    info_img_path = request.form.get('IMG_PATH')
    new_img = str(info_img_path) + os.path.sep + str(info_img_name)
    info = select(info_img_name)
    # print(new_img)
    # new_img_json = {'data': "data:;base64," + return_img_stream(new_img),
    #                 'name': info_img_name,
    #                 'path': info_img_path,
    #                 'ero': info.ero,
    #                 'bare': info.bare,
    #                 'hentai': info.hentai,
    #                 'handsome': info.handsome,
    #                 'sex': info.sex}
    new_img_json = {'data': "data:;base64," + return_img_stream(new_img)}
    return new_img_json


# @app.route('/change', methods=['GET', 'POST'])
# def change_sql():
#     info_items = request.form.to_dict()
#     info_img_name = request.form.get('img_name')
#     info_img_ero = request.form.get('ero')
#     inf_img_bare = request.form.get('bare')
#     inf_img_hentai = request.form.get('hentai')
#     inf_img_handsome = request.form.get('handsome')
#     inf_img_sex = request.form.get('sex')
#     print(info_items)
#     info_items.pop("img_name")
#     change_info(info_img_name, info_items)
#     # print("info are ", info_img_name, info_img_ero, inf_img_bare, inf_img_hentai, inf_img_handsome, inf_img_sex)
#     return index()


def select(img_info: str):
    """
    工具函数:
    根据文件名从数据库中搜索对应的信息
    :param img_info: 文件名
    :return: 数据库对象
    """
    info = ImageInformation.query.filter_by(img_name=img_info).first()
    return info


def change_info(img_info: str, ch_info_dict: dict):
    """
    工具函数:
    根据文件名从数据库中修改对应的信息
    :param img_info: 文件名,
    :param ch_info_dict: 需修改的键与值,
    :return: None
    """
    legal_list = ['ero', 'bare', 'hentai', 'handsome', 'sex']
    info = ImageInformation.query.filter_by(img_name=img_info).first()
    for item in ch_info_dict:
        if item in legal_list:
            setattr(info, item, ch_info_dict[item])
        else:
            pass
    db.session.commit()


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
