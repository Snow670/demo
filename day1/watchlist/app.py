from flask import Flask,url_for,render_template
app = Flask(__name__)


# @app.route('/index/<name>')
# def index(name):
#     print(url_for('index',name='哈哈哈'))
#     return '首页%s'%name


@app.route('/')
def index():
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
    return render_template('index.html',name=name,movies=movies)