from flask_cors import CORS
from userDAO import user_signup, user_login, user_get
from Util import jwtTokenUtil
from bookDAO import getBooks, getBkidByBknamedao, updateBookdao

import os
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() + '/EPUBS'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"/*": {"origins": "*"}})  # 跨域问题


@app.route('/api/')
def hello_world():
    return 'Hello World!'


@app.route('/api/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        authority = request.json['authority']
        avatar = request.json['avatar']
        name = request.json['name']
        res = user_signup(username, password, authority, avatar, name)
        return res
    else:
        return 'GET'


@app.route('/api/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        res = user_login(username, password)
        return res
    else:
        return 'GET'


@app.route('/api/getUser', methods=['POST', 'GET'])
def getUser():
    if request.method == 'POST':
        username = request.json['username']
        print("20", username)
        res = user_get(username)
        return res
    else:
        return 'GET'


from userDAO import getAllUsersDAO


@app.route('/api/getAllUsers', methods=['POST', 'GET'])
def getAllUsers():
    if request.method == 'POST':
        data = getAllUsersDAO()
        res_data = {
            'message': '请求成功',
            'code': 200,
            'data': data
        }
        return res_data
    else:
        return 'GET'


# 发送包含token的json, 返回json user + token 否则返回username=-1
@app.route('/api/tokenCheck', methods=['POST', 'GET'])
def tkCheck():
    # request.headers.get("X-Token")
    ans = jwtTokenUtil.Decode(request.args.get("token"))
    if ans == -1:
        res_data = {
            'message': '登录状态失效',  # token不合法
            'code': 50001,
            'data': ''
        }
        return res_data
    temp = {}
    temp.update(user_get(ans['username']))
    data = {'userinfo': temp, 'token': jwtTokenUtil.MakeCode(ans['username'])}
    temp.pop('_id')
    res_data = {
        'message': 'token合法',
        'code': 200,
        'data': data
    }
    return res_data


@app.route('/api/getBooks', methods=['POST'])
def getBook():
    sortby = request.json['sortby']
    findfor = request.json['findfor']
    star = request.json['star']
    state = request.json['state']
    return getBooks(sortby, findfor, star, state)


from bookDAO import getSingleBookDAO


@app.route('/api/getBook', methods=['POST'])
def getSingleBook():
    bkid = request.json['bkid']
    data = getSingleBookDAO(bkid)
    res_data = {
        'message': 'ok',
        'code': 200,
        'data': data
    }
    return res_data


@app.route('/api/getBkidByBkname', methods=['POST'])
def getBkidByBkname():
    bkname = request.json['bkname']
    return getBkidByBknamedao(bkname)


@app.route('/api/updateBook', methods=['POST'])
def updateBook():
    bkid = request.json.get('bkid')
    bkname = request.json.get('bkname')
    bkauthor = request.json.get('bkauthor')
    bkclass = request.json.get('bkclass')
    bkstate = request.json.get('bkstate')
    bkinfo = request.json.get('bkinfo')
    bkimg = request.json.get('bkimg')
    bkchapter = request.json.get('bkchapter')
    return updateBookdao(bkid, bkname, bkauthor, bkclass, bkstate, bkinfo, bkimg, bkchapter)


ALLOWED_EXTENSIONS = {'epub'}


# app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


from epubUpload import updateSingleBook


@app.route('/api/uploadepub', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save("./EPUBS/" + filename)
            return updateSingleBook("./EPUBS/" + filename)


from bookDAO import viewbook


@app.route('/api/view', methods=['GET', 'POST'])
def viewBook():
    bkid = request.json['bkid']
    viewbook(bkid)
    res_data = {
        'message': '记录写入成功',
        'code': 200,
        'data': ''
    }
    return res_data


from bkviewDAO import bkviewDAO_history


@app.route('/api/history', methods=['GET', 'POST'])
def history():
    bkid = request.json['bkid']
    data = bkviewDAO_history(bkid)
    res_data = {
        'message': '本书浏览记录查询成功',
        'code': 200,
        'data': data
    }
    return res_data


from bkviewDAO import top4month

@app.route('/api/top4month', methods=['GET', 'POST'])
def top4mon():
    data = top4month()
    res_data = {
        'message': '本书浏览记录查询成功',
        'code': 200,
        'data': data
    }
    return res_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
