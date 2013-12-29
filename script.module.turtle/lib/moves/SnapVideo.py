'''
Created on Nov 5, 2011

@author: ajju
'''
import re
from common import XBMCInterfaceUtils, DataObjects, AddonUtils, ExceptionHandler
import sys
from TurtleContainer import AddonContext
from common.HttpUtils import HttpClient
from common.DataObjects import ListItem
import xbmcgui #@UnresolvedImport

class Snapper(object):
    def __init__(self, snapper_Tag):
        modulePath = snapper_Tag['module']
        functionName = snapper_Tag['function']
        self.__video_id_regex_list = []
        for videoIdTag in snapper_Tag.findAll('video-id'):
            self.__video_id_regex_list.append(videoIdTag['regex'])
        self.__is_playlist = False
        if snapper_Tag.has_key('playlist') and snapper_Tag['playlist'] == 'true':
            self.__is_playlist = True
        components = modulePath.split('.')
        module = __import__(modulePath)
        if components is not None and isinstance(components, list):
            for index in range(1, len(components)):
                module = getattr(module, components[index])
        
        self.__snapper_module = module
        self.__getVideoInfo = getattr(module, functionName)
        self.getVideoHostingInfo = getattr(module, 'getVideoHostingInfo')
        print 'Snapper loaded = ' + modulePath

    def isPlaylistSnapper(self):
        return self.__is_playlist
    
    def isVideoHostedByYou(self, video_url):
        isVideoHoster = False
        videoId = self.getVideoId(video_url)
        if videoId is not None:
            isVideoHoster = True
        return isVideoHoster
    
    def getVideoInfo(self, video_url):
        videoInfo = None
        videoId = self.getVideoId(video_url)
        if videoId is not None:
            videoInfo = self.__getVideoInfo(videoId)
        return videoInfo
    
    def getVideoId(self, video_url):
        videoId = None
        for video_id_regex in self.__video_id_regex_list:
            match = re.compile(video_id_regex).findall(video_url + '&')
            if len(match) > 0:
                videoId = match[0]
                break
        return videoId

snappers = None

def __initializeSnappers():
    snapper_filepath = AddonUtils.getCompleteFilePath(AddonContext().addonPath, 'snapvideo', 'snappers.xml')
    if not AddonUtils.doesFileExist(snapper_filepath):
        snapper_filepath = AddonUtils.getCompleteFilePath(AddonContext().turtle_addonPath, 'lib/snapvideo', 'snappers.xml')
        print 'Loading snappers.xml from turtle library... ' + snapper_filepath
    snappers_xml = AddonUtils.getBeautifulSoupObj(snapper_filepath)
    global snappers
    if snappers is not None:
        return snappers
    snappers = []
    for snapperTag in snappers_xml.findAll('snapper', attrs={'enabled':'true'}):
        snappers.append(Snapper(snapperTag))
    return snappers
    
    
def findVideoHostingInfo(video_url):
    for snapper in __initializeSnappers():
        if(snapper.isVideoHostedByYou(video_url)):
            return snapper.getVideoHostingInfo()

def findVideoInfo(video_url):
    for snapper in __initializeSnappers():
        if not snapper.isPlaylistSnapper():
            video_info = snapper.getVideoInfo(video_url)
            if video_info is not None:
                return video_info
            
def findPlaylistInfo(playlist_url):
    for snapper in __initializeSnappers():
        if snapper.isPlaylistSnapper():
            video_info = snapper.getVideoInfo(playlist_url)
            if video_info is not None:
                return video_info

def addVideoHostingInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addVideoHostingInfo_in_item'), items, 'Retrieving video info', 'Failed to retrieve video information, please try again later')

def __addVideoHostingInfo_in_item(item):
    videoHostingInfo = findVideoHostingInfo(item.get_moving_data()['videoUrl'])
    item.set_xbmc_list_item_obj(XBMCInterfaceUtils.updateListItem_With_VideoHostingInfo(videoHostingInfo, item.get_xbmc_list_item_obj()))
        
def addVideoInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addVideoInfo_in_item'), items, 'Retrieving video info', 'Failed to retrieve video information, please try again later')

def __addVideoInfo_in_item(item):
    __processAndAddVideoInfo__(item, item.get_moving_data()['videoUrl'])


def addEmbeddedVideoInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addEmbeddedVideoInfo_in_item__'), items, 'Retrieving video info', 'Failed to retrieve video information, please try again later')


def __addEmbeddedVideoInfo_in_item__(item):
    video_url = item.get_moving_data()['videoUrl']
    if findVideoHostingInfo(video_url) == None:
        html = HttpClient().getHtmlContent(video_url)
        __processAndAddVideoInfo__(item, html)
    else:
        __processAndAddVideoInfo__(item, video_url)


def __processAndAddVideoInfo__(item, data):
    video_info = findVideoInfo(data)
    if video_info is None:
        raise Exception(ExceptionHandler.VIDEO_PARSER_NOT_FOUND, 'Video information is not found. Please check other sources.')
    if video_info.is_video_stopped():
        raise Exception(ExceptionHandler.VIDEO_STOPPED, 'Video is either removed or not found. Please check other links.')
    XBMCInterfaceUtils.updateListItem_With_VideoInfo(video_info, item.get_xbmc_list_item_obj())
    qual = int(AddonContext().addon.getSetting('playbackqual'))
    video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_HD_1080)
    if video_strm_link == None or qual != 0:
        video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_HD_720)
        if video_strm_link == None or qual == 2:
            video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_SD)
            if video_strm_link == None:
                video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_LOW)
    item.get_moving_data()['videoStreamUrl'] = video_strm_link
    
    
def addPlaylistVideosInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    for item in items:
        videoItems = __processPlaylistAndAddVideoItem__(item)
        if videoItems is not None and len(videoItems) > 0:
            items.remove(item)
            items.extend(videoItems)
    
def __processPlaylistAndAddVideoItem__(item):
    playlist = findPlaylistInfo(item.get_moving_data()['videoUrl'])
    if playlist is not None:
        videoItems = []
        part = 0
        for videoUrl in playlist:
            part = part + 1
            item = ListItem()
            item.add_moving_data('videoUrl', videoUrl)
            item.set_next_action_name('Play')
            xbmcListItem = xbmcgui.ListItem(label='Video ' + str(part))
            item.set_xbmc_list_item_obj(xbmcListItem)
            videoItems.append(item)
        return videoItems
