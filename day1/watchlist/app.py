from flask import Flask,url_for
app = Flask(__name__)


@app.route('/index/<name>')
def index(name):
    print(url_for('index',name='哈哈哈'))
    return '首页%s'%name