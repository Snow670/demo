from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
import os,sys,click


WIN = sys.platform.startswith('win')
if WIN:
    prefix = "sqlite:///"    #windows平台
else:
    prefix = "sqlite:////"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#models 数据层
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))






#views 视图函数
@app.route('/')
def index():
    # name = 'Snow'
    # movies = [
    #     {'title':'aa','year':'2020'},
    #     {'title':'bb','year':'2019'},
    #     {'title':'cc','year':'2018'},
    #     {'title':'dd','year':'2017'},
    #     {'title':'ee','year':'2020'},
    #     {'title':'ff','year':'2010'},
    #     {'title':'gg','year':'2019'},
    # ]
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user=user,movies=movies)



#自定义命令
#建立空数据库
@app.cli.command()   #注册为命令
@click.option('--drop',is_flag=True,help='先删除再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成')  



#添加数据
@app.cli.command()
def forge():
    name = 'Snow'
    movies = [
        {'title':'aa','year':'2020'},
        {'title':'bb','year':'2019'},
        {'title':'cc','year':'2018'},
        {'title':'dd','year':'2017'},
        {'title':'ee','year':'2020'},
        {'title':'ff','year':'2010'},
        {'title':'gg','year':'2019'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('导入数据完成')