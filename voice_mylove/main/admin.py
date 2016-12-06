#coding=utf-8
from django.contrib import admin
from .models import VoiceRecord

@admin.register(VoiceRecord)
class VoiceRecordAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'voice_url', 'share_id', 'log_time')
