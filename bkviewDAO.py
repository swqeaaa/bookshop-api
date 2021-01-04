import pymongo

host = '127.0.0.1'
conn = pymongo.MongoClient(host, 27017)
liangyv = conn.liangyv
liangyv.authenticate('liangyv', '1234')
bkvdb = liangyv.bkview


def bkviewDAO_update(bkid, today):
    print(today)
    todaydb = bkvdb.find_one({'bkid': bkid, 'date': today})
    if todaydb is None:
        bkvdb.insert_one({'bkid': bkid, 'date': today, 'num': 1})
    else:
        todaydb['num'] = todaydb['num'] + 1
        bkvdb.update({'bkid': bkid, 'date': today}, todaydb)


def bkviewDAO_history(bkid):
    list = bkvdb.find({'bkid': bkid})
    data = []
    for i in list:
        i.pop("_id")
        data.append(i)
    data = sorted(data, key=lambda e: e.__getitem__('date'))
    siz = min(len(data), 30)  # 取最后30个
    data = data[-siz:]
    # print(data)
    return data


host = '127.0.0.1'
conn = pymongo.MongoClient(host, 27017)
liangyv = conn.liangyv
liangyv.authenticate('liangyv', '1234')
bkdb = liangyv.books

import time
import datetime


def top4month():
    cursor = bkdb.find({})
    list = []
    for i in cursor:
        i.pop('_id')
        cursor2 = bkvdb.find({'bkid': i['bkid']})
        tmp = 0
        for j in cursor2:
            today = datetime.date.today()
            if abs(j['date'] - int(time.mktime(today.timetuple()))) <= 6 * 86400:
                tmp = tmp + j['num']
        list.append({'bkid': i['bkid'],'bkname': i['bkname'],'bkimg': i['bkimg'], 'num': tmp})
    list = sorted(list, key=lambda e: e.__getitem__('num'), reverse=True)
    part1list = []
    part2list = {}

    for i in range(0, 4):
        part1list.append(list[i])
        part2list[list[i]['bkid']] = (bkviewDAO_history(list[i]['bkid']))

    data = {'part1list': part1list, 'part2list': part2list}
    return data


if __name__ == '__main__':
    # bkviewDAO_history(66746)
    top4month()
