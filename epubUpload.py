from ebooklib import epub
from Util.unzipUtil import unzip
import os

import pymongo

host = '127.0.0.1'
conn = pymongo.MongoClient(host, 27017)
liangyv = conn.liangyv
liangyv.authenticate('liangyv', '1234')
bkdb = liangyv.books

from lxml import etree


def getFiles(dir, suffix):  # 查找根目录，文件后缀
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename)  # =>文件名,文件后缀
            if suf == suffix:
                res.append(os.path.join(root, filename))  # =>吧一串字符串组合成路径
    return res


def getbkinfo(url):
    f = open(url, encoding='utf-8')
    content = f.read()
    f.close()
    content = bytes(bytearray(content, encoding='utf-8'))
    html = etree.HTML(content)
    result = html.xpath("/html/body/div/ul/li[2]/text()")
    return str(result[0])


from chapterDAO import getChapterForBkid


def updateSingleBookHelper(file):
    bookid = file[8:-5]
    unzip(file, './static/' + bookid)
    i = 0
    for file2 in getFiles('./static/' + bookid, '.xhtml'):
        os.rename(file2, './static/' + bookid + '/' + str(i) + '.xhtml')
        i = i + 1

    book = epub.read_epub(file)
    booktodb = {
        "bkname": book.get_metadata('DC', 'title')[0][0],
        "bkauthor": book.get_metadata('DC', 'creator')[0][0],
        "bkclass": '类型',
        "bkstate": '完结',
        "bkstar": 5,
        "bkinfo": getbkinfo("./static/" + bookid + "/" + str(i - 1) + ".xhtml"),
        "bkimg": '/static/' + bookid + '/cover.jpg',
        "bkid": int(bookid),
        "url": '/static/' + bookid + '/0.xhtml',
        'bkviewnum': 0,
        'bksize': i - 2
    }
    bkdb.insert_one(booktodb)

    getChapterForBkid(int(bookid))#为这本书配套其章节名&章节URL

    print("thread mession completed.")


import threading


def updateSingleBook(file):
    bookid = file[8:-5]
    if bkdb.find_one({"bkid": int(bookid)}) is not None:
        res_data = {
            'message': '本书已存在',
            'code': 400,
            'data': ''
        }
        return res_data
    res_data = {
        'message': '上传成功',
        'code': 200,
        'data': ''
    }
    t1 = threading.Thread(target=updateSingleBookHelper, args=(file,)) #多线程
    t1.start()
    return res_data


def updateBooks():
    for file in getFiles("./EPUBS/", '.epub'):  # =>查找以.epub结尾的文件
        updateSingleBook(file)


if __name__ == '__main__':
    updateBooks()

# 封面 /static/bookvname/cover.jpg
# 作者 book.get_metadata('DC', 'creator')[0][0]
# 标题 book.get_metadata('DC', 'title')[0][0]
