import pymongo
import uuid

host = '127.0.0.1'
conn = pymongo.MongoClient(host, 27017)
liangyv = conn.liangyv
liangyv.authenticate('liangyv', '1234')
bkdb = liangyv.books

from lxml import etree
from json import loads


def getbkinfo(bkid, url, size):
    # xxx0.xhtml
    print(url[0:-8])
    commonurl = url[1:-7]
    f = open(url, encoding='utf-8')
    content = f.read()
    f.close()
    content = bytes(bytearray(content, encoding='utf-8'))
    html = etree.HTML(content)
    list = []
    for i in range(1, size):
        name = html.xpath("/html/body/ul/li[" + str(i) + "]/a/text()")[0]
        dict = {
            'chapterid': str(i),
            'chaptername': name,
            'chapterurl': (commonurl + str(i) + '.xhtml')
        }
        list.append(dict)
    onebook = bkdb.find_one({'bkid': bkid})
    onebook['bkchapter'] = list
    # print(list)
    bkdb.update({'bkid': bkid}, onebook)


def getChapterForBkid(bkid):
    onebook = bkdb.find_one({'bkid': bkid})
    url = '.' + onebook['url']
    size = onebook['bksize']
    getbkinfo(bkid, url, size)


# 获得每章的章节名 章节url
if __name__ == '__main__':
    list = bkdb.find({})
    for onebook in list:
        if onebook['bkchapter'] != [] and onebook['bkchapter'] is not None:
            bkid = onebook['bkid']
            getChapterForBkid(bkid)
