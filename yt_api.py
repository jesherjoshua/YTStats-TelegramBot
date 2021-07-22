# FUNCTIONS MODULE TO GET DATA

import re
from pytube import YouTube
from pytube import extract
from pyyoutube import Api
import json as js
import time
import datetime
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import urlparse


fhand = open('yt_api_key.txt')
key = None
for i in fhand:
    key = i.strip()
api = Api(api_key=key)


def get_id(link):
    url = link
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
    uhand = opener.open(url)
    html = uhand.read().decode()
    soup = bs(html, 'html.parser')
    ch_id = re.findall('channel_id=(\S+?")', html)
    ext_id = re.findall('"externalId":(\S+?")', html)
    f_id = None
    for j in range(0, 1):
        for i in ch_id:
            f_id = i[:-1]
    return f_id


def get_stats(channelId):
    get_stats = api.get_channel_info(channel_id=channelId)
    stats = get_stats.items[0].to_dict()
    title = stats['snippet']['title']
    desc = stats['snippet']['description']
    country = stats['snippet']['country']
    if (stats['statistics']['hiddenSubscriberCount'] == True):
        sub_count = 'Hidden'
    else:
        sub_count = stats['statistics']['subscriberCount']
    vid_count = stats['statistics']['videoCount']
    return[title, desc, country, sub_count, vid_count]


def get_vid_info(a):
    url = a
    yt = YouTube(url)
    channel_name = yt.author
    title = yt.title
    length = yt.length
    views = yt.views
    upload_date = yt.publish_date
    date = upload_date.strftime('%d/%m/%Y')
    return[channel_name, title, length, views, date]


def get_rating(url):
    vinfo = api.get_video_by_id(video_id=extract.video_id(url))
    j = vinfo.items[0].to_dict()
    if (j['status']['publicStatsViewable'] == True):
        lcount = j['statistics']['likeCount']
        dlcount = j['statistics']['dislikeCount']
        ccount = j['statistics']['commentCount']
    else:
        lcount = 'Hidden'
        dlcount = 'Hidden'
        ccount = 'Hidden'
    return[lcount, dlcount, ccount]


def get_thumbnail(url):
    yt = YouTube(url)
    turl = yt.thumbnail_url
    return turl
