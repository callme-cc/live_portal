#coding:utf-8

from django.views.generic import *
from django.http import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from live_portal.models import *
from datetime import timedelta
from django.utils import timezone


class ShowView(TemplateView):
    template_name = 'live_portal_show.html'
    merged_tag_mapping = {
        # u'歌手': [u'鱼音绕梁'],
        # u'生活': [u'元气领域'],
        u'户外': [u'Outdoor', u'鱼行天下', u'户外直播', u'全民户外', u'元气领域'],
        u'秀场': [u'全民星秀', u'娱乐联萌', u'鱼音绕梁', u'鱼秀'],
        u'体育': [u'体育频道', u'体育竞技'],
        u'主机游戏': [u'单机主机', u'主机游戏', u'单机游戏'],
        u'放映厅': [u'一起看', u'第九放映室'],
        u'': [],
    }

    def get(self, request, tag):
        if not tag or tag == u'所有直播':
            # rooms = Room.objects.all()
            # NOTE: MySQL generate timestamp with UTC+8 timezone, but here timezone.now() gets UTC.
            rooms = Room.objects.all()
            tag = u'所有直播'
        elif tag in self.merged_tag_mapping:
            rooms = Room.objects.filter(tag__in=self.merged_tag_mapping[tag])
        else:
            rooms = Room.objects.filter(tag=tag)

        rooms_top = rooms.filter(modification_time__gte=timezone.now()+timedelta(hours=7)).order_by('audience_count').reverse()

        page_index = request.GET.get('page', 1)
        try:
            p_rooms = Paginator(rooms_top, 20).page(page_index)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p_rooms = Paginator(rooms_top, 20).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p_rooms = Paginator(rooms_top, 20).page(paginator.num_pages)


        return render(request, self.template_name,
                {'tag':tag, 'p_rooms':p_rooms})

class HomeView(TemplateView):
    template_name = 'live_portal_show.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/show/");
