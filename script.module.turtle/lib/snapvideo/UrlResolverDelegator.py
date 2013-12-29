'''
Created on Nov 21, 2012

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
import urlresolver  # @UnresolvedImport

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('')
    video_hosting_info.set_video_hosting_name('UrlResolver by t0mm0')
    return video_hosting_info

def retrieveVideoInfo(videoUrl):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(videoUrl)
    try:
        sources = []
        hosted_media = urlresolver.HostedMediaFile(url=videoUrl)
        sources.append(hosted_media)
        source = urlresolver.choose_source(sources)
        stream_url = ''
        if source: 
            stream_url = source.resolve()
    
        video_info.set_video_stopped(False)
        video_info.set_video_image('')
        video_info.set_video_name(' ')
        video_info.add_video_link(VIDEO_QUAL_SD, stream_url)
    except:
        video_info.set_video_stopped(True)
    return video_info

