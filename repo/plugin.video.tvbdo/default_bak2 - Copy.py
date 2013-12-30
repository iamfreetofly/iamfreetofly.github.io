import httplib
import urllib,urllib2,re,sys,urlparse
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import json
import urlresolver
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc
from urlparse import urljoin

import datetime
import time
ADDON = xbmcaddon.Addon(id='plugin.video.tvbdo')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "TVBdo"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-41910477-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.6" #<---- PLUGIN VERSION
#domainlist = [" ", " ", " "]
#domain = domainlist[int(ADDON.getSetting('domainurl'))]
def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        #addDir('Search',' ',4,' ')
        addDir('TVB Dramas','http://tvbdo.com/category/tvb-drama/',2,'')
        #addDir('HK Movies','http://tvbdo.com/category/hk-movies/',13,'')
        addDir('HK Variety','http://tvbdo.com/category/hk-variety/',2,'')
        addDir('HKTV','http://tvbdo.com/category/hktv/',2,'')
        addDir('Mainland Dramas','http://tvbdo.com/category/mainland-dramas/',2,'')
        addDir('Planet Discovery','http://tvbdo.com/category/planet-discovery/',14,'')

        
def INDEX(url,newmode):
    #try:
        link = GetContent(url)
        
        vidmode=5
        
        if(newmode==13):
                vidmode=10
        elif(newmode==14):
                vidmode=11
        
        try:
            link = link.encode("UTF-8")
        except: pass
        
        newlink = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        listcontent=re.compile('<div id="main">(.+?)</body>').findall(newlink)
        
        match=re.compile('<img src="(.+?)" [^>]*>(.+?)<h2 class="title"><a href="(.+?)" [^>]*>(.+?)</a></h2>').findall(listcontent[0])

        for (vimg,vtmp,vurl,vname) in match:
            try:
                  vname = vname.replace('&#8211;','-')
                  addDir(vname,vurl,vidmode,vimg)
            except:
                  addDir(vname.decode("utf-8"),vurl,vidmode,vimg)
                  
        pagecontent=re.compile('<div class="wp-pagenavi"><span class="pages">(.+?)</div>').findall(newlink)            
        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)" class="(.+?)">(.+?)</a>').findall(pagecontent[0])
                for (vurl,vtmp,vname) in match5:
                    try:
                        addDir('page: ' + vname,vurl,2,'')
                    except:
                        addDir('page: ' + vname.decode('utf-8'),vurl,2,'')
    #except: pass

def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = ' '+ searchText
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
        link = ''.join(link.splitlines()).replace('\'','"').replace('\t','').replace('\\','')
        partlist=re.compile('var parts = \{"1":(.+?)></script>').findall(link)
        #print ("============================ POSTING partlist ============================")
        #print (partlist)
        partctr=0
        if(len(partlist)>0):
               partlink=re.compile('<iframe [^>]*src="(.+?)"></iframe></div>').findall(partlist[0])
               print ("============================ POSTING partlink ============================")
               print (partlink)
               if(len(partlink) > 1):
                       playList = ''
                       for vlink in partlink:
                              partctr=partctr+1
                              addDir(name.decode("utf-8") + " Part " + str(partctr),vlink,3,"")
                              playList = playList + vlink +";#"
                              
                       print ("============================ POSTING playList ============================")
                       print (playList)

                       addDir('------------->[B]PLAY ALL[/B]<------------- [I]Watch all ' + str(partctr) + ' parts[/I]',playList,3,'')

        return partctr
    
def CheckParts(url,name):
	if(Parts(url,name) < 2):
		loadVideos(url,name)

def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))



def Episodes(url,name,newmode):
    #try:
        link = GetContent(url)
        try:
            link = link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        
        findEpisodeLink = re.compile('<h2><strong><a href="(.+?)">(.+?)</a>').findall(newlink)

        for (vurl,tmp) in findEpisodeLink:
            try:
                findEpisodes(vurl,name,newmode)
            except:
                findEpisodes(url_fix(vurl),name,newmode)

    #except: pass


def findEpisodes(url,name,newmode):
    #try:
        link = GetContent(url)
        try:
            link = link.encode("UTF-8")
        except: pass
        
        newlink = ''.join(link.splitlines()).replace('\t','')

        listcontent=re.compile('<div id="main">(.+?)</body>').findall(newlink)

        if(newmode==5):
                vidmode=11
        else:
                vidmode=9

        match=re.compile('<h2 class="title"><a href="(.+?)" [^>]*>(.+?)</a></h2>').findall(urllib.unquote(listcontent[0]).decode('utf-8'))

        print ("============================ POSTING match ============================")
        print match
        
        for (vurl,vname) in match:
            vname = vname.replace('&#8211;','-')
            try:
                addDir(vname,url_fix(vurl),vidmode,"")
            except:
                addDir(vname.decode("utf-8"),url_fix(vurl),vidmode,"")

    #except: pass


def Episodes2(url,name,newmode):
    #try:
        link = GetContent(url)
        try:
            link = link.encode("UTF-8")
        except: pass
        
        newlink = ''.join(link.splitlines()).replace('\t','')

        
        match = re.compile('<div class="entry-embed"><iframe src="(.+?)" [^>]*></iframe>').findall(newlink)

        print ("============================ POSTING match ============================")
        print match

        for (vurl) in match:
            try:
                addDir('Watch ' + name,vurl,15,"")
            except:
                addDir('Watch ' + name.decode("utf-8"),url_fix(vurl),15,"")

    #except: pass


def PlayUrlSource(url1,name):
    #try:

        GA("LoadVideo","NA")
        #xbmc.executebuiltin("XBMC.Notification(Please Wait!, Loading video link into XBMC Media Player,5000)")
        link = GetContent(url1)
        try:
            link = link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','').replace('href="/file','href="http://www.putlocker.com/file')
        
        match = re.compile('<div id="file_title" [^>]*><a href="(.+?)" [^>]*><strong>').findall(newlink)

        print ("============================ POSTING match ============================")
        print match

        for (vurl) in match:
            try:
                ResolveUrl(vurl,name)
            except: pass
        
    #except: pass 


def ResolveUrl(url,name):
        sources = []
        try:
            label=name
            hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
        
            sources.append(hosted_media)
        except:
            print 'Error while trying to resolve %s' % url

        source = urlresolver.choose_source(sources)
        print "urlresolving" + url
        if source:
            vidlink = source.resolve()
        else:
            vidlink =""

        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(vidlink)


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

def GetJSON(data,url,referr,cj):
    if cj==None:
        cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache')]
    usock=opener.open(data,url)
    data = json.loads(usock)
    usock.close()
    return data
	   
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
    print videoType + '=' + videoId
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
           GA("LoadVideo",name)
           links=url.split(';#')

           print ("============================ POSTING links ============================")
           print links

           vlinkplayList=''
           vlinkplayList2=''
           
           qualityval = ["360p(MP4)","360p(FLV)","480p(FLV)","720p(MP4)"]
           qualityval2 = ["360p(MP4) - English Subs","360p(FLV) - English Subs","480p(FLV) - English Subs","720p(MP4) - English Subs"]

           print ("============================ POSTING lengthlinks ============================")
           print len(links)
           newrange = len(links) - 1

           for i in range(newrange):
               link = GetContent(links[i])

               newlink = ''.join(link.splitlines()).replace('\t','').replace('mp4360p','file').replace('flv360p','file').replace('flv480p','file').replace('mp4720p','file')
      
               match=re.compile('<script type="text\/javascript">var videos = \{"Chinese":\{(.+?)\}').findall(urllib.unquote(newlink).decode('utf-8'))
               match2=re.compile('<script type="text\/javascript">[^>]*"English":\{(.+?)\}').findall(urllib.unquote(newlink).decode('utf-8'))

               framecontent = json.dumps(match).replace('\\','').replace('""','",\;"')
               framecontent2 = json.dumps(match2).replace('\\','').replace('""','",\;"')

               embedlink = re.compile('\;(.+?)\;').findall(urllib.unquote(framecontent).decode('utf-8'))
               embedlink2 = re.compile('\;(.+?)\;').findall(urllib.unquote(framecontent2).decode('utf-8'))

               vlink = re.compile('"file":"(.+?)"\,').findall(embedlink[0])
               vlink2 = re.compile('"file":"(.+?)"\,').findall(embedlink2[0])

               vlinkplayList = vlinkplayList + str(vlink) +";#"
               vlinkplayList2 = vlinkplayList2 + str(vlink2) +";#"
           
           qctr=0
           qctr2=0
           if(len(links) == 1):
               vlink = re.compile('"file":"(.+?)"\,').findall(embedlink)
               for vname in vlink:
                   if(len(vlink) > 0):
                       addLink(qualityval[qctr],urllib.unquote(vlink[0]),8,"","")
                       qctr=qctr+1
                       
               if match2:
                   vlink2 = re.compile('"file":"(.+?)"\,').findall(embedlink2)
                   for vname2 in vlink:
                       if(len(vlink2) > 0):
                           addLink(qualityval2[qctr2],urllib.unquote(vlink2[0]),8,"","")
                           qctr2=qctr2+1
                           
           if(len(links) > 1):

               print ("============================ POSTING vlinkplayList ============================")
               print vlinkplayList

               print ("============================ POSTING vlinkplayList2 ============================")
               print vlinkplayList2

               allPartlinks = vlinkplayList.split(';#')
               print ("============================ POSTING allPartlinks ============================")
               print allPartlinks

               partlinks1 = allPartlinks[0]
               partlinks1 = partlinks1.split(', ')
               print ("============================ POSTING partlinks1 ============================")
               print partlinks1
               print type(partlinks1)
           
               partlinks2 = allPartlinks[1]
               partlinks2 = partlinks2.split(', ')
               print ("============================ POSTING partlinks2 ============================")
               print partlinks2
           
               partlinks3 = allPartlinks[2]
               partlinks3 = partlinks3.split(', ')
               print ("============================ POSTING partlinks3 ============================")
               print partlinks3

               allPartlinks2 = vlinkplayList2.split(';#')
               print ("============================ POSTING allPartlinks2 ============================")
               print allPartlinks2

               partlinks1a = allPartlinks2[0]
               print ("============================ POSTING partlinks1a ============================")
               print partlinks1a
           
               partlinks2a = allPartlinks2[1]
               print ("============================ POSTING partlinks2a ============================")
               print partlinks2a
           
               partlinks3a = allPartlinks2[2]
               print ("============================ POSTING partlinks3a ============================")
               print partlinks3a

               parts123Links =  partlinks1[0] + ";#" + partlinks2[0] + ";#" + partlinks3[0]
               print ("============================ POSTING parts123Links ============================")
               print parts123Links

               addLink(qualityval[0],parts123Links,14,"","")


           if(len(links) > 10):
               qctr3=0
               qctr4=0
               #vlink = re.compile('"file":"(.+?)"\,').findall(embedlink[0])
               for vname in vlink:
                   if(len(vlink) > 0):
                       addLink(qualityval[qctr],urllib.unquote(parts123Links),14,"","")
                       qctr3=qctr3+1
                       
               if match2:
                   #vlink2 = re.compile('"file":"(.+?)"\,').findall(embedlink2[0])
                   for vname2 in vlink:
                       if(len(vlink2) > 0):
                           addLink(qualityval2[qctr2],urllib.unquote(vlink2[0]),14,"","")
                           qctr4=qctr4+1

                           
           #else:
                 #  match=re.compile('<script type="text\/javascript">(.+?)var language').findall(urllib.unquote(newlink))
                 #  if(len(match) > 0):
                 #          loadVideos(match[0],name)
                 #  else:  
                  #         d = xbmcgui.Dialog()
                  #         d.ok('Not Implemented','Sorry this video site is ',' not implemented yet')

def PLAYLIST_VIDEOLINKS(name,url):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = url.split(';#')
        print "linksurl" + str(url)
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                loadPlaylist(videoLink,name)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                #print percent
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False   
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('videourl: ' + str(playList), 'One or more of the playlist items','Check links individually.')
        return ok

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
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
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
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
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
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'  =========================='
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
            print build
            print PLATFORM
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
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
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
print "mode is:" + str(mode)
if mode==None or url==None or len(url)<1:

        HOME()
elif mode==2:
        GA("INDEX",name)
        INDEX(url,mode)
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
       GA("Episodes",name)
       Episodes2(url,name,mode)
elif mode==11:
       CheckParts(url,name)
elif mode==12:
       PLAYLIST_VIDEOLINKS(url,name)
elif mode==13:
        GA("INDEX",name)
        INDEX(url,mode)
elif mode==14:
        GA("INDEX",name)
        INDEX(url,mode)
elif mode==15:
       PlayUrlSource(url,name)
elif mode==16:
       PLAYLIST_VIDEOLINKS(name,url)

xbmcplugin.endOfDirectory(int(sysarg))
