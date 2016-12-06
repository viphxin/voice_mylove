#coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class VoiceRecord(models.Model):
    """
    @des:语音合成记录
    """
    nickname = models.CharField(_(u'昵称(用来唯一标识用户)'), max_length=10, db_index=True)
    short_desc = models.CharField(_(u'简短描述'), max_length=20)
    text = models.CharField(_(u'内容'), max_length=512)
    voice_url = models.CharField(_(u"音频cdn地址"), max_length=255)
    share_id = models.CharField(_(u"分享出去的ID"), max_length=32, unique=True)
    log_time = models.DateTimeField(_(u'时间'), auto_now_add=True)

    class Meta:
        db_table = "voicerecord"
        verbose_name = _(u'语音合成记录')
        verbose_name_plural = verbose_name