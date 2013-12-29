'''
Created on Oct 29, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_LOW, \
    VIDEO_QUAL_SD, VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080
from common import HttpUtils
import re
import urllib

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.automotivefinancingsystems.com/images/icons/socialmedia_youtube_256x256.png')
    video_hosting_info.set_video_hosting_name('YouTube')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info.set_video_image('http://i.ytimg.com/vi/' + video_id + '/default.jpg')
        html = HttpUtils.HttpClient().getHtmlContent(url='http://www.youtube.com/watch?v=' + video_id + '&fmt=18')
        stream_map = None
        html = html.replace('\\u0026', '&')
        match = re.compile('url_encoded_fmt_stream_map=(.+?)&').findall(html)
        
        if len(match) == 0:
            stream_map = (re.compile('url_encoded_fmt_stream_map": "(.+?)"').findall(html)[0]).replace('\\/', '/').split('url=')
        else:
            stream_map = urllib.unquote(match[0]).decode('utf8').split('url=')
        
        if re.search('status=fail', html):
            video_info.set_video_stopped(True)
            return video_info
        if stream_map == None:
            video_info.set_video_stopped(True)
            return video_info
            
        for attr in stream_map:
            if attr == '':
                continue
            parts = urllib.unquote(attr).decode('utf8').split('&qual')
            url = parts[0]
            qual = re.compile('&itag=(\d*)').findall(parts[1])[0]
            if(qual == '13'):#176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '17'):#176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '36'):#320x240
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '5'):#400\\327226
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '34'):#480x360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '6'):#640\\327360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '35'):#854\\327480 HD
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '18'):#480x360 MP4
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '22' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):#1280x720 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '37' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):#1920x1080 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '38'):#4096\\3272304 EPIC MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '43' and video_info.get_video_link(VIDEO_QUAL_SD) is None):#4096\\3272304 WEBM
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '44' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):#4096\\3272304 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '45' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):#4096\\3272304 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '120' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):#New video qual
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            else:#unknown quality
                video_info.add_video_link(VIDEO_QUAL_SD, url)

            video_info.set_video_stopped(False)
    except:
        video_info.set_video_stopped(True)
    return video_info


def retrievePlaylistVideoItems(playlistId):
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('media:player'):
        videoUrl = str(media['url'])
        videoItemsList.append(videoUrl)
    return videoItemsList
    
def retrieveReloadedPlaylistVideoItems(playlistId):
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('track'):
        videoUrl = media.findChild('location').getText()
        videoItemsList.append(videoUrl)
    return videoItemsList
    
    
