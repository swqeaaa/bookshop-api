import pymongo
import uuid

host = '127.0.0.1'
conn = pymongo.MongoClient(host, 27017)
liangyv = conn.liangyv
liangyv.authenticate('liangyv', '1234')
bkdb = liangyv.books
bkvdb = liangyv.bkview
import random

if __name__ == '__main__':
    cursor = bkdb.find({})
    bkidl = []
    for i in cursor:
        bkidl.append(i['bkid'])
    for i in range(0, 9):
        nowbk = bkidl[i]
        for j in range(0, 7):
            bkvdb.insert_one({
                'bkid': nowbk,
                'date': 1606579200 - j * 86400,
                'num':random.randint(0,50)
            })
