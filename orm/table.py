from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////erolibrary.db'
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
        return '<User %r>' % self.img_name
