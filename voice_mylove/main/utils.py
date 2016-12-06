#coding=utf-8
import requests, datetime, json
from cdnhelper import upyunclient

TOCKEN_URL = "https://openapi.baidu.com/oauth/2.0/token"
GEN_VOICE_URL = "http://tsn.baidu.com/text2audio"
CLIENT_ID = "jSEsPZ7spMO3tLkxGOlcdvAY"
CLIENT_SECRIT = "98878a594096cf6e7eaf54c8cbcbe058"
tocken_global = None

def get_accesstocken():
    """
    获取百度的登录凭证
    :return:
    """
    global tocken_global
    if tocken_global and tocken_global['t'] + datetime.timedelta(seconds=tocken_global['data']['expires_in']) > datetime.datetime.now():
        #直接返回
        return tocken_global["data"]['access_token']
    else:
        #重新获取
        r = requests.post(url=TOCKEN_URL, data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRIT
        })
        if r.status_code == 200:
            tocken_global = {
                't': datetime.datetime.now(),
                'data': json.loads(r.content)
            }
            return tocken_global["data"]['access_token']
        else:
            print r.content
            raise Exception("get_accesstocken error")

def get_voice_url(text):
    """
    获取语音合成文件并上传到cdn
    :param text:
    :return:
    """
    r = requests.post(GEN_VOICE_URL, data={
        "tex": text.encode("utf-8"),
        "lan": "zh",
        "tok": get_accesstocken(),
        "ctp": 1,
        "cuid": CLIENT_ID
    })
    if r.status_code == 200 and r.headers['Content-type'] == 'audio/mp3':
        cdn_url = upyunclient.uploadData(r.content, upyunclient.genFileName("voice_mylove/") + ".mp3", None)
        return cdn_url
    else:
        print text
        raise Exception("get_voice_url error")


if __name__ == "__main__":
    get_voice_url(u"黄家驹降级")