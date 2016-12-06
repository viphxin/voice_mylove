#coding=utf-8
"""
cdn 上传帮助
pip install requests
pip install upyun
"""
import random, time
import upyun
from StringIO import StringIO

class UpyunHelper(object):
    def __init__(self, bucket, username, password):
        self.up = upyun.UpYun(bucket, username=username, password=password, timeout=60)

    def genFileName(self, prex):
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0,100)
        return prex + fn

    def uploadFile(self, path, name, headers):
        """
        上传成功返回空的{}
        :param path:
        :param name:
        :param headers:
        :return:
        """
        res = None
        with open(path, 'rb') as f:
            res = self.up.put(name, f, checksum=True, headers=headers)
        return res

    def uploadData(self, data, name, headers):
        res = None
        # f = StringIO()
        # f.write(data)
        # f.seek(0)

        res = self.up.put(name, data, checksum=True, headers=headers)
        return "http://dragonz.b0.upaiyun.com/%s" % (name, )

upyunclient = UpyunHelper("dragonz", "viphxin", "VIPhxin163")

if __name__ == "__main__":
    #cdnurl = "http://dragonz.b0.upaiyun.com/%s" % (name, )
    name = upyunclient.genFileName("test/")
    # print upyunclient.uploadFile("/home/huangxin/下载/python-sdk-master/requirements.txt", name + ".txt", None)
    print upyunclient.uploadData("dddddddd\r\n", name + ".txt", None)