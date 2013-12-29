'''
Created on Oct 29, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720
from common import HttpUtils
import re
import urllib
#try:
#    import json
#except ImportError:
#    import simplejson as json

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://aux.iconpedia.net/uploads/1687271053.png')
    video_hosting_info.set_video_hosting_name('Dailymotion')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://www.dailymotion.com/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link)
        sequence = re.compile('"sequence":"(.+?)"').findall(html)
        newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')
        #        jsonObj = json.loads(newseqeunce, encoding='utf-8')
        #        print jsonObj
        imgSrc = re.compile('og:image" content="(.+?)"').findall(html)
        if(len(imgSrc) == 0):
            imgSrc = re.compile('/jpeg" href="(.+?)"').findall(html)
        dm_low = re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
        dm_high = re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
        
        video_info.set_video_image(imgSrc[0])
        video_info.set_video_stopped(False)
        
        if(len(dm_high) == 0 and len(dm_low) == 1):
            video_info.add_video_link(VIDEO_QUAL_SD, dm_low[0])
        elif(len(dm_low) == 0 and len(dm_high) == 1):
            video_info.add_video_link(VIDEO_QUAL_HD_720, dm_high[0])
        else:
            video_info.add_video_link(VIDEO_QUAL_SD, dm_low[0])
            video_info.add_video_link(VIDEO_QUAL_HD_720, dm_high[0])
    except: 
        video_info.set_video_stopped(True)
    return video_info

def retrievePlaylistVideoItems(playlistId):
    html = HttpUtils.HttpClient().getHtmlContent(url='http://www.dailymotion.com/playlist/' + playlistId)
    mediaLines = re.compile('<a dm:context="/playlist/' + playlistId + '[a-zA-Z0-9_\-]*" title="(.+?)" href="(.+?)"').findall(html)
    videoItemsList = []
    for mediaTitle, mediaUrl in mediaLines: #@UnusedVariable
        videoItemsList.append('http://www.dailymotion.com' + mediaUrl)
    return videoItemsList
