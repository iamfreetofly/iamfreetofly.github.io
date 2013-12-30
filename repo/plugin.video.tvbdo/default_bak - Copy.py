# -*- coding: cp1252 -*-
import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc

import datetime
import time
ADDON = xbmcaddon.Addon(id='plugin.video.tvbdo')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "TVBDO"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-41910477-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.6" #<---- PLUGIN VERSION


def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        #addDir('Search','http://www.khmeravenue.com/',4,'http://yeuphim.net/images/logo.png')
        addDir('TVB Drama','http://tvbdo.com/tvb-drama/',2,'')
        addDir('HK Movies','http://tvbdo.com/category/hk-movies/',2,'')
        addDir('HK Variety','http://tvbdo.com/category/hk-variety/',2,'')
        
def INDEX(url):
    #try:
        link = GetContent(url)
        try:
            link = link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<article id="main-article">(.+?)</article>').findall(newlink)
        match=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)<h2 class="entry-title"><a href="(.+?)" rel="bookmark" title="(.+?)">(.+?)</a></h2>').findall(listcontent[0])
        for (vimg,vtmp2,vurl,vtmp,vname) in match:
            try:
                  vname = vname.replace('&#8211;','-')
                  addDir(vname,vurl,5,vimg)
            except:
                  addDir(vname.decode("utf-8"),vurl,5,vimg)
        pagecontent=re.compile('<div class="clear"></div></article>(.+?)</div>').findall(newlink)            
        if(len(pagecontent)>0):
                match5=re.compile("<a href='(.+?)' class='(.+?)'>(.+?)</a>").findall(pagecontent[0])
                for (vurl,vtmp,vname) in match5:
                    try:
                        addDir("page: " + vname,vurl,2,"")
                    except:
                        addDir('page: ' + vname.decode("utf-8"),vurl,2,'')
    #except: pass

def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://yeuphim.net/movie-list.php?str='+ searchText
        INDEX(url)
    except: pass

def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<aclass="widget-title" href="(.+?)"><imgsrc="(.+?)" alt="(.+?)"').findall(newlink)
        if(len(match) >= 1):
                for vLink,vpic,vLinkName in match:
                    addDir(vLinkName,vLink,5,vpic)
        match=re.compile('<strong>&raquo;</strong>').findall(link)
        if(len(match) >= 1):
            startlen=re.compile("<strongclass='on'>(.+?)</strong>").findall(newlink)
            url=url.replace("/page/"+startlen[0]+"/","/page/"+ str(int(startlen[0])+1)+"/")
            addDir("Next >>",url,6,"")

def Mirrors(url,name):
    try:
        if(CheckRedirect(url)):
                MirrorsThe(name,url)
        else:
                link = GetContent(url)
                newlink = ''.join(link.splitlines()).replace('\t','')
                match=re.compile('<b>Episode list </b>(.+?)</table>').findall(newlink)
                mirrors=re.compile('<div style="margin: 10px 0px 5px 0px">(.+?)</div>').findall(match[0])
                if(len(mirrors) >= 1):
                        for vLinkName in mirrors:
                            addDir(vLinkName.encode("utf-8"),url,5,'')
    except: pass
	
def Parts(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','').replace('{','<')
        partlist=re.compile('<"1":(.+?)</script>').findall(link)
        print ("============================ POSTING partlist ============================")
        print (partlist)        
        partctr=0
        if(len(partlist)>0):       
               partlink=re.compile('<iframe [^>]*src=\\\\"(.+?)">').findall(partlist[0])
               print ("============================ POSTING partlink ============================")
               print (partlink)
               if(len(partlink) > 1):
                       for vlink in partlink:
                              partctr=partctr+1
                              print ("============================ POSTING vlink ============================")
                              print vlink.replace("\\","")
                              addDir(name.decode("utf-8") + " Part " + str(partctr),vlink.replace("\\",""),3,"")
                              #addDir(name.decode("utf-8") + " Part " + str(partctr),urllib.unquote(vlink),3,"")
        return partctr
		
def CheckParts(url,name):
	if(Parts(url,name) < 2):
		loadVideos(url,name)
def Episodes(url,name,newmode):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div class="entry-content">(.+?)</div>').findall(newlink)
        if(newmode==5):
                vidmode=11
        else:
                vidmode=9
        match=re.compile('<a class="button small white" href="(.+?)" target="_blank">(.+?)</a>').findall(listcontent[0])
        for (vurl,vname) in match:
            try:
                vname = vname.replace('&#8211;','-')
                addDir(vname,vurl,vidmode,"")
            except:
                addDir(vname.decode("utf-8"),vurl,vidmode,"")
    #except: pass

def GetEpisodeFromVideo(url,name):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<center><a href="(.+?)"><font style="(.+?)">(.+?)</font></a></center>').findall(newlink)
        Episodes(listcontent[0][0]+"list-episode/",name,5)

def Geturl(strToken):
        for i in range(20):
                try:
                        strToken=strToken.decode('base-64')
                except:
                        return strToken
                if strToken.find("http") != -1:
                        return strToken

def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = ""
    print (videoType + '=' + videoId)
    print ("============================ POSTING videoID ============================")
    print videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
           #GA("LoadVideo",name)
           link=GetContent(url)
           newlink = ''.join(link.splitlines()).replace('\t','').replace('\'','"').replace('}','>').replace('mp4360p','file').replace('flv360p','file').replace('flv480p','file').replace('var language','<tmp>')
           #match=re.compile('<script type="text\/javascript">(.+?)</script>').findall(newlink)
           #match=re.compile('<div id="player"><embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
           match=re.compile('<script type="text\/javascript">var videos = [^>]*"file":"(.+?)"[^>]*\}').findall(newlink)
           print ("============================ POSTING match ============================")
           print match
           if(len(match) > 0):
                   framecontent = GetContent(match[0])
                   qualityval = ["360p(MP4)","360p(FLV)","480p(FLV)"]
                   qctr=0
                   embedlink = re.compile('var videos = [^>]*"file":"(.+?)"[^>]*\}').findall(framecontent)
                   #embedlink=re.compile('<script [^>]*var videos = [^>]*"file":["\']?([^>^"^\']+)["\']?[^>]*>').findall(framecontent)
                   #embedlink=re.compile('var videos = ["\']?([^>^"^\']+)["\']?[^>]*').findall(framecontent)
                   print ("============================ POSTING embedlink ============================")
                   print embedlink
                   for vname in embedlink:
                         vlink=re.compile('"file":"(.+?)"\,').findall(urllib.unquote(vname))
                         print ("============================ POSTING vlink ============================")
                         print vlink
                         if(len(vlink) > 0):
                             addLink(qualityval[qctr],urllib.unquote(vlink[0]),8,"","")
                         qctr=qctr+1
           else:
                   match=re.compile('<div id="player"><embed src=[^>]*file=(.+?)\&[^>]*></div>').findall(newlink)
                   if(len(match) > 0):
                           loadVideos(match[0],name)
                   else:  
                           d = xbmcgui.Dialog()
                           d.ok('Not Implemented','Sorry this video site is ',' not implemented yet')

#def loadVideos(url,name):
#           #GA("LoadVideo",name)
#           link=GetContent(url)
#           newlink = ''.join(link.splitlines()).replace('\t','').replace('\'','"').replace('}','>').replace('mp4360p','file').replace('flv360p','file').replace('flv480p','file').replace('var language','<tmp>')
#           match=re.compile('<div id="player"><embed src=[^>]*file=(.+?)\&[^>]*></div>').findall(newlink)
#           if(len(match) > 0):
#                   loadVideos(urllib.unquote(match[0]),name)
#           else:
#                   d = xbmcgui.Dialog()
#                   d.ok('Not Implemented','Sorry this video site is ',' not implemented yet')

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print ("============================ POSTING TRACK EVENT ============================")
                        send_request_to_google_analytics(utm_track)
                    except:
                        print ("============================  CANNOT POST TRACK EVENT ============================")
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print ("============================ POSTING ANALYTICS ============================")
            send_request_to_google_analytics(utm_url)
            
        except:
            print ("================  CANNOT POST TO ANALYTICS  ================") 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print ('======================= more than ====================')
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print ('==========================   '+PATH+' '+VERSION+'  ==========================')
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print (build)
            print (PLATFORM)
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print ("============================ POSTING APP LAUNCH TRACK EVENT ============================")
                send_request_to_google_analytics(utm_track)
            except:
                print ("============================  CANNOT POST APP LAUNCH TRACK EVENT ============================")
checkGA()

def addLink(name,url,mode,iconimage,mirrorname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))+"&mirrorname="+urllib.quote_plus(mirrorname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param



params=get_params()
url=None
name=None
mode=None
formvar=None
mirrorname=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        mirrorname=urllib.unquote_plus(params["mirrorname"])
except:
        pass

sysarg=str(sys.argv[1])
print ("mode is:" + str(mode))
if mode==None or url==None or len(url)<1:

        HOME()
elif mode==2:
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
        loadVideos(url,mirrorname)
elif mode==4:
        SEARCH()
elif mode==5:
       GA("Episodes",name)
       Episodes(url,name,mode)
elif mode==6:
       SearchResults(url)
elif mode==7:
       Episodes(url,name,mode)
elif mode==8:
        playVideo("direct",url)
elif mode==9:
       GetEpisodeFromVideo(url,name)
elif mode==10:
       Episodes2(url,name)
elif mode==11:
       CheckParts(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
