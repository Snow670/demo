from flask import Flask,url_for,render_template,request,redirect,flash
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
app.config['SECRET_KEY'] = '1903_dev'

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
@app.route('/',methods=["post","get"])
def index():    
    movies = Movie.query.all()
    if request.method == "POST":
        # 获取表单的数据
        title = request.form.get('title')
        year = request.form.get('year')

        # 验证数据
        if not title or not year or len(title)>60 or len(year)>4:
            flash("输入错误")
            return redirect(url_for('index'))
        # 将数据保存到数据库
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("创建成功")
        return redirect(url_for('index'))
    return render_template('index.html',movies=movies)


#更新/movie/edit
@app.route('/movie/edit/<int:movie_id>',methods=["post","get"])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        # 获取表单的数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(title)>60 or len(year)>4:
            flash("输入错误")
            return redirect(url_for('edit'),movie_id=movie_id)
        movie.title=title
        movie.year=year
        db.session.commit()
        flash('电影更新完成')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)


#删除/movie/delete
@app.route('/movie/delete/<int:movie_id>',methods=["post","get"])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除完成")
    return redirect(url_for('index'))






#自定义命令
#建立空数据库
@app.cli.command()   #注册为命令
@click.option('--drop',is_flag=True,help='先删除再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成')  



#向空数据库中添加数据
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


#错误处理函数
@app.errorhandler(404)
def page_not_find(e):
    return render_template('404.html')


#模板上下文处理函数
@app.context_processor
def common_user():
     user = User.query.first()
     return dict(user=user)