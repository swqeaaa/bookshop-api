import pymongo
import uuid

host = '127.0.0.1'
conn = pymongo.MongoClient(host, 27017)
liangyv = conn.liangyv
liangyv.authenticate('liangyv', '1234')
bkdb = liangyv.books


def getSingleBookDAO(bkid):
    book = bkdb.find_one({'bkid': bkid})
    book.pop('_id')
    return book


def getBooks(sortby, findfor, star, state):
    findfor = str(findfor)
    result = bkdb.find({})
    a = []
    for i in result:  # i是值不是指针
        i.pop("_id")
        if findfor == '':
            a.append(i)
        else:
            flag = 0
            for j in i.values():  # 在值中找findfor
                strj = str(j)
                if findfor in strj:
                    flag = 1
                    break
            if (flag == 1):
                a.append(i)  # 如果值中有这个, 就把这本书(dict)放到答案中
    newa1 = []
    if star is None:
        newa1 = a
    else:
        for i in a:
            if i['bkstar'] == star:
                newa1.append(i)
    newa2 = []
    if state == '':
        newa2 = newa1
    else:
        for i in newa1:
            if i['bkstate'] == state:
                newa2.append(i)
    if sortby == '':
        newa3 = newa2
    else:
        newa3 = sorted(newa2, key=lambda e: e.__getitem__(sortby[1:]), reverse=False if (sortby[0] == '+') else True)
    data = {'items': newa3, 'total': len(newa3)}
    res_data = {
        'message': 'ok',
        'code': 200,
        'data': data
    }
    return res_data


def updateBookdao(bkid, bkname, bkauthor, bkclass, bkstate, bkinfo, bkimg, bkchapter):
    newbook = {
        'bkname': bkname,
        'bkauthor': bkauthor,
        'bkclass': bkclass,
        'bkstate': bkstate,
        'bkinfo': bkinfo,
        'bkimg': bkimg,
        'bkid': bkid,
        'bkchapter': bkchapter
    }
    newbook2 = []
    for key, value in newbook.items():
        if value is None or value == '':
            newbook2.append({key: value})

    bkdb.update({'bkid': bkid}, {"$set": newbook2})
    res_data = {
        'message': '修改书籍信息成功',
        'code': 200,
        'data': ''
    }
    return res_data


def getBkidByBknamedao(bkname):
    a = bkdb.find_one({'bkname': bkname})
    res_data = {
        'message': '此书id查询成功',
        'code': 200,
        'data': a['bkid']
    }
    return res_data


import time
import datetime
from bkviewDAO import bkviewDAO_update


def viewbook(bkid):
    a = bkdb.find_one({'bkid': bkid})
    a['bkviewnum'] = a['bkviewnum'] + 1
    bkdb.update({'bkid': bkid}, a)
    today = datetime.date.today()
    today_time = int(time.mktime(today.timetuple()))
    bkviewDAO_update(bkid, today_time)


if __name__ == '__main__':
    viewbook(66746)
