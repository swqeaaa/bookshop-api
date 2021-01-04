import zipfile

'''
基本格式：zipfile.ZipFile(filename[,mode[,compression[,allowZip64]]])
mode：可选 r,w,a 代表不同的打开文件的方式；r 只读；w 重写；a 添加
compression：指出这个 zipfile 用什么压缩方法，默认是 ZIP_STORED，另一种选择是 ZIP_DEFLATED；
allowZip64：bool型变量，当设置为True时可以创建大于 2G 的 zip 文件，默认值 True；

'''
def unzip(filepath,folder_abs):
    zip_file = zipfile.ZipFile(filepath)
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件

    for f in zip_list:
        zip_file.extract(f, folder_abs)  # 循环解压文件到指定目录
    zip_file.close()  # 关闭文件，必须有，释放内存