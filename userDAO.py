import pymongo
from Util import jwtTokenUtil

host = '127.0.0.1'
client = pymongo.MongoClient(host, 27017)
liangyv = client.liangyv
liangyv.authenticate('liangyv', '1234')
users = liangyv.users


def user_signup(username, password, authority, avatar,name):
    user = {
        'username': username
    }
    result = users.find_one(user)
    if result == None:
        data = {
            'username': username,
            'password': password,
            'authority': authority,
            'avatar': avatar,
            'name':name
        }
        try:
            users.insert_one(data)
        except:
            res_data = {
                'message': '数据库写入失败',
                'code': 500,
                'data': ''
            }
            return res_data
        finally:
            res_data = {
                'message': '注册成功',
                'code': 200,
                'data': ''
            }
            return res_data
    else:
        res_data = {
            'message': '用户名存在',
            'code': 400,
            'data': ''
        }
        return res_data


def user_login(username, password):
    user = {
        'username': username
    }
    result = users.find_one(user)
    if result == None:
        res_data = {
            'message': '用户名或密码错误',
            'code': 400,
            'data': ''
        }
        return res_data
    else:
        if result['password'] == password:
            result.pop("_id")
            # 去掉mongodb的毒瘤东西
            token = jwtTokenUtil.MakeCode(result['username'])
            data= {'userinfo':result, 'token':token}
            res_data = {
                'message': '登陆成功',
                'code': 200,
                'data': data
                # // 存在cookie里的token
            }
            # print("token",token)
            return res_data
        else:
            res_data = {
                'message': '用户名或密码错误',
                'code': 400,
                'data': ''
            }
            return res_data


def user_get(username):
    user = {
        'username': username
    }
    result = users.find_one(user)
    return result

def getAllUsersDAO():
    result=users.find({})
    data=[]
    for i in result:
        i.pop('_id')
        data.append(i)
    return data