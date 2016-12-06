#coding=utf-8
import requests, json, hashlib, time
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from utils import get_voice_url
from main.models import VoiceRecord

def home(request):
    """
    主页
    :param request:
    :return:
    """
    return TemplateResponse(request, template="home.html")

def addRecord(request):
    """
    添加语音记录
    :param request:
    :return:
    """
    nickname = request.POST.get("nickname", None)
    short_desc = request.POST.get("short_desc", None)
    text = request.POST.get("text", None)
    checkcode = request.POST.get("checkcode", None)
    print request.POST
    if nickname and short_desc and text and checkcode and checkcode.lower() == request.session.get('checkcode', u"攻击"):
        if len(nickname) > 10 or len(short_desc) > 10 or len(text) > 512:
            return HttpResponse(json.dumps({"error": "text length max exceed!!!!!!!!"}))
        cdn_url = get_voice_url(text)
        #入库
        md5sign = hashlib.md5()
        md5sign.update(text.encode("utf-8"))
        md5sign.update("%s" % time.time())

        share_id = md5sign.hexdigest()
        VoiceRecord.objects.create(
            nickname=nickname,
            short_desc=short_desc,
            text=text,
            voice_url=cdn_url,
            share_id=share_id
        )
        #跳转到播放页
        return HttpResponseRedirect("/share/%s/" % share_id)
    else:
        return HttpResponse(json.dumps({"error": "param error!!!!!!!!"}))

def share(request, share_id):
    try:
        obj = VoiceRecord.objects.get(share_id=share_id)
        return TemplateResponse(request, template="share.html", context={'cdn_url': obj.voice_url,
                                                                         "nickname": obj.nickname,
                                                                         "log_time": obj.log_time,
                                                                         "short_desc": obj.short_desc})
        # return render_to_response("share.html", context={'cdn_url': obj.voice_url,
        #                                                  "nickname": obj.nickname,
        #                                                  "log_time": obj.log_time,
        #                                                  "short_desc": obj.short_desc})
    except:
        return home(request)