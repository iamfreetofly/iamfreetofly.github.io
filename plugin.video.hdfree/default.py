import httplib
import urllib,urllib2,re,sys
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

ADDON = xbmcaddon.Addon(id='plugin.video.hdfree')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
GA_PRIVACY = ADDON.getSetting('ga_privacy') == "true"
DISPLAY_MIRRORS = ADDON.getSetting('display_mirrors') == "true"

UASTR = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0"
PATH = "HDFree"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-41910477-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0" #<---- PLUGIN VERSION
domainlist = ["hdfree.co"]
domain = domainlist[int(ADDON.getSetting('domainurl'))]
domainprefix = ["http://"]
strdomain = "http://hdfree.co/"

HEADERS = {
        'User-Agent':    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept':                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cache-Control': 'no-transform'
}

def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        #addDir('Search','http://www.khmeravenue.com/',4,'http://yeuphim.net/images/logo.png')
##        if ADDON.getSetting('list_recent_updates') == "true":
##            addDir('Recent Updates','http://'+domain+'/recently-updated/',2,'')
##        if ADDON.getSetting('list_english_subtitles') == "true":
##            addDir('English Subtitles','http://'+domain+'/english/&sort=date',7,'')
        if ADDON.getSetting('list_hk_dramas') == "true":
            addDir('HK Dramas','http://'+domain+'/browse/hongkong/dramas/',2,'')
        if ADDON.getSetting('list_hk_movies') == "true":
            addDir('HK Movies','http://'+domain+'/browse/hongkong/movies/',12,'')
        if ADDON.getSetting('list_hk_shows') == "true":
            addDir('HK TVShows','http://'+domain+'/browse/hongkong/tvshow/',2,'')
        if ADDON.getSetting('list_china_dramas') == "true":
            addDir('Chinese(China) Dramas','http://'+domain+'/browse/chinese/dramas/',2,'')
        if ADDON.getSetting('list_china_movies') == "true":
            addDir('Chinese(China) Movies','http://'+domain+'/browse/chinese/movies/',12,'')
        if ADDON.getSetting('list_china_shows') == "true":
            addDir('Chinese(China) TVShows','http://'+domain+'/browse/chinese/tvshow/',2,'')
        if ADDON.getSetting('list_taiwan_dramas') == "true":
            addDir('Taiwanese Dramas','http://'+domain+'/browse/taiwanese/dramas/',2,'')
        if ADDON.getSetting('list_taiwan_movies') == "true":
            addDir('Taiwanese Movies','http://'+domain+'/browse/taiwanese/movies/',12,'')
        if ADDON.getSetting('list_taiwan_shows') == "true":
            addDir('Taiwanese TVShows','http://'+domain+'/browse/taiwanese/tvshow/',2,'')
##        if ADDON.getSetting('list_english_dramas') == "true":
##            addDir('English Dramas','http://'+domain+'/browse/english/dramas/',2,'')
##        if ADDON.getSetting('list_english_movies') == "true":
##            addDir('English Movies','http://'+domain+'/browse/english/movies/',12,'')
##        if ADDON.getSetting('list_english_shows') == "true":
##            addDir('English TVShows','http://'+domain+'/browse/english/tvshow/',2,'')
        if ADDON.getSetting('list_korean_dramas') == "true":
            addDir('Korean Dramas','http://'+domain+'/browse/korean/dramas/',2,'')
        if ADDON.getSetting('list_korean_movies') == "true":
            addDir('Korean Movies','http://'+domain+'/browse/korean/movies/',12,'')
        if ADDON.getSetting('list_korean_shows') == "true":
            addDir('Korean TVShows','http://'+domain+'/browse/korean/tvshow/',2,'')
        if ADDON.getSetting('list_japanese_dramas') == "true":
            addDir('Japanese Dramas','http://'+domain+'/browse/japanese/dramas/',2,'')
        if ADDON.getSetting('list_japanese_movies') == "true":
            addDir('Japanese Movies','http://'+domain+'/browse/japanese/movies/',12,'')
        if ADDON.getSetting('list_japanese_shows') == "true":
            addDir('Japanese TVShows','http://'+domain+'/browse/japanese/tvshow/',2,'')
        if ADDON.getSetting('list_english_dramas') == "true":
            addDir('Thailand Dramas','http://'+domain+'/browse/thailand/dramas/',2,'')
        if ADDON.getSetting('list_english_movies') == "true":
            addDir('Thailand Movies','http://'+domain+'/browse/thailand/movies/',12,'')
        if ADDON.getSetting('list_english_shows') == "true":
            addDir('Thailand TVShows','http://'+domain+'/browse/thailand/tvshow/',2,'')

def INDEX(url):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','').replace('<span aria-hidden="true">\xc2\xab</span>','Previous').replace('<span aria-hidden="true">\xc2\xbb</span>','Next').replace('<strong style="color:Red">','').replace('</strong>','').replace('&#39;','\'').replace('amp;','')
        listcontent=re.compile('<body>(.+?)</body>').findall(newlink)
        match=re.compile('<div class="v-grid">(.+?)<a href="(.+?)" [^>]*><img alt="(.+?)" src="(.+?)" [^>]*></a>').findall(listcontent[0])
        for (vtmp,vurl,vname,vimg) in match:
            try:
                  addDir(vname,"http://"+domain+"/watch-online"+vurl,7,vimg)
            except:
                  addDir(vname.decode("utf-8"),"http://"+domain+"/watch-online"+vurl,7,vimg)
        pagecontent=re.compile('<ul class="pagination">(.+?)</ul>').findall(newlink)
        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)"[^>]*>(.+?)</a>').findall(pagecontent[0])
                for vurl,vname in match5:
                    addDir('[COLOR yellow]page: [/COLOR]' + cleanPage(vname),"http://"+domain+vurl,2,"")
    #except: pass

def INDEX2(url):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','').replace('<span aria-hidden="true">\xc2\xab</span>','Previous').replace('<span aria-hidden="true">\xc2\xbb</span>','Next').replace('<strong style="color:Red">','').replace('</strong>','').replace('&#39;','\'').replace('amp;','')
        listcontent=re.compile('<body>(.+?)</body>').findall(newlink)
        match=re.compile('<div class="v-grid">(.+?)<a href="(.+?)" [^>]*><img alt="(.+?)" src="(.+?)" [^>]*></a>').findall(listcontent[0])
        for (vtmp,vurl,vname,vimg) in match:
            try:
                  addDir(vname,"http://"+domain+"/watch-online"+vurl,3,vimg)
            except:
                  addDir(vname.decode("utf-8"),"http://"+domain+"/watch-online"+vurl,3,vimg)
        pagecontent=re.compile('<ul class="pagination">(.+?)</ul>').findall(newlink)
        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)"[^>]*>(.+?)</a>').findall(pagecontent[0])
                for vurl,vname in match5:
                    addDir('[COLOR yellow]page: [/COLOR]' + cleanPage(vname),"http://"+domain+vurl,13,"")
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
	
def decodeurl(encodedurl):
    tempp9 =""
    tempp4="100108100114971099749574853495756564852485749575656"
    strlen = len(encodedurl)
    temp5=int(encodedurl[strlen-4:strlen],10)
    encodedurl=encodedurl[0:strlen-4]
    strlen = len(encodedurl)
    temp6=""
    temp7=0
    temp8=0
    while temp8 < strlen:
        temp7=temp7+2
        temp9=encodedurl[temp8:temp8+4]
        temp9i=int(temp9,16)
        partlen = ((temp8 / 4) % len(tempp4))
        partint=int(tempp4[partlen:partlen+1])
        temp9i=((((temp9i - temp5) - partint) - (temp7 * temp7)) -16)/3
        temp9=chr(temp9i)
        temp6=temp6+temp9
        temp8=temp8+4
    return temp6
	
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
                            if DISPLAY_MIRRORS:
                                addDir(vLinkName.encode("utf-8"),url,5,'')
                            else:
                               loadVideos(url, vLinkName.encode("utf-8")) 

    except: pass
	
def Parts(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        partlist=re.compile('<ul class="listew">(.+?)</ul>').findall(link)
        partlist=re.compile('<li>(.+?)<\/li>').findall(partlist[0])
        totalpart=0
        for partconent in partlist:
               print "partconent", partconent
               totalpart=totalpart+1
               partctr=0
               partlink=re.compile('<a href="(.+?html)">').findall(partconent)
               mirror=re.compile('^(.+?): .*').findall(partconent)
               full=re.compile('<b.+?(Full).+?/b>').findall(partconent) 
               if(len(partlink) > 0):
                          mirrorname="Unknown"
                          partname = ""
                          if(len(mirror)>0):
                              mirrorname=mirror[0]
                          for vlink in partlink:
                              partctr=partctr+1
                              if len(full)<1:
                                     partname = " Part " + str(partctr) +"/" + str(len(partlink))

                              mirrortitle = mirrorname+" "+partname
                              if(len(partlist) > 1 and totalpart>0):
                                     if DISPLAY_MIRRORS:
                                         addDir(name +"@"+mirrortitle,vlink,3,"")
                                     else:
                                         loadVideos(vlink,"@" + mirrortitle + " " + name)


        return totalpart
		
def CheckParts(url,name):
	if(Parts(url,name) < 2):
		loadVideos(url,name)
		
def Episodes(url,name,newmode):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\n\t','').replace('&#39;','\'').replace('amp;','')
        listcontent=re.compile('<div style="border-bottom:1px [^>]*>Show all available episodes</div>(.+?)<div style="border-bottom:1px [^>]*>Share with your friends to support us[^>]*</div>').findall(newlink)
        if(newmode==7):
            vidmode=3
        else:
            vidmode=9
        match=re.compile('<a href="(.+?)" [^>]* title="(.+?)">(.+?)Watch Online(.+?)</a>').findall(listcontent[0])
        for (vurl,vname,vtmp,vtmp2) in match:
            try:
                  addDir(vname,"http://"+domain+vurl,vidmode,"")
                  break
            except:
                  addDir(vname.decode("utf-8"),"http://"+domain+vurl,vidmode,"")
        pagecontent=re.compile('<div class="wp-pagenavi" align=center>(.+?)</div>').findall(newlink)
        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)" class="(.+?)" title="(.+?)">(.+?)</a>').findall(pagecontent[0])
                for vurl,vtmp,vname,vtmp2 in match5:
                    addDir(cleanPage(vname),vurl,newmode,"")

    #except: pass

def GetEpisodeFromVideo(url,name):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div align="center">(.+?)<div style=[^>]*>').findall(newlink)
        if listcontent:
            match=re.compile('<a href="(.+?)"><b>(.+?)</b>').findall(listcontent[0])
            if match:
                for (vurl,vname) in match:
                    try:
                        addDir("Episode: " + vname,vurl,11,"")
                    except:
                        addDir("Episode: " + vname.decode("utf-8"),vurl,11,"")
            else:
                listcontent=re.compile('<center><a href="(.+?)"><font style="(.+?)">(.+?)</font></a></center>').findall(newlink)
                Episodes(listcontent[0][0]+"list-episode/",name,5)
        else:
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
		
def postContent(url,data,referr):
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', UASTR),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache'),
                         ('Host','player.phim47.com')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response
	
def Videosresolve(url,name):
        #try:
           newlink=url
           if (newlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(url+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(url)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                req = urllib2.Request(link)
                req.add_header('User-Agent', UASTR)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"video_url":"(.+?)",').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                vidlink=urllib2.unquote(dm_low[0]).decode("utf8")
           elif (newlink.find("cloudy") > -1):
                pcontent=GetContent(newlink)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                filecode = re.compile('flashvars.file="(.+?)";').findall(pcontent)[0]
                filekey = re.compile('flashvars.filekey="(.+?)";').findall(pcontent)[0]
                vidcontent="https://www.cloudy.ec/api/player.api.php?file=%s&key=%s"%(filecode,urllib.quote_plus(filekey))
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('url=(.+?)&').findall(pcontent)[0]
                vidlink=urllib.unquote_plus(urlcode)
           elif (newlink.find("videomega") > -1):
                refkey= re.compile('\?ref=(.+?)&dk').findall(newlink+"&dk")[0]
                vidcontent="http://videomega.tv/iframe.php?ref="+refkey
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('if\s*\(!validstr\){\s*document.write\(unescape\("(.+?)"\)\);\s*}').findall(pcontent)[0]
                vidcontent=urllib.unquote_plus(urlcode)
                vidlink = re.compile('file:\s*"(.+?)",').findall(vidcontent)[0]
           elif (newlink.find("video44") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('file:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
                     media_url = re.compile('url:\s*"(.+?)"').findall(link)
                vidlink = media_url[0]
           elif (newlink.find("videobug") > -1):
                link=urllib.unquote_plus(GetContent(newlink))
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)
                if(len(media_url)==0):
                    media_url = re.compile('{file:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
                    media_url = re.compile('file:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
                    media_url = re.compile('dll:\s*"(.+?)"').findall(link)
                    if len(media_url) > 0 and "http" not in media_url[0]:
                        media_url[0] = "http://videobug.se" + media_url[0]
                if(len(media_url)==0):
                    media_url = re.compile('link:\s*"([^"]+?//[^"]+?/[^"]+?)"').findall(link)
                    if("http://" in Geturl(media_url[0])):
                       media_url[0] = Geturl(media_url[0])
                vidlink = urllib.unquote(media_url[0].replace(' ', '+'))
           elif (newlink.find("play44") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
           elif (newlink.find("byzoo") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
           elif (newlink.find("vidzur") > -1 or newlink.find("videofun") > -1 or newlink.find("auengine") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                op = re.compile('playlist:\s*\[(.+?)\]').findall(link)[0]
                urls=op.split("{")
                for rows in urls:
                     if(rows.find("url") > -1):
                          murl= re.compile('url:\s*"(.+?)"').findall(rows)[0]
                          media_url=urllib.unquote_plus(murl)
                vidlink = media_url
           elif (newlink.find("cheesestream") > -1 or newlink.find("yucache") > -1):
                link=GetContent(newlink)
                link=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('<meta property="og:video" content="(.+?)"/>').findall(link)[0]
           elif(newlink.find("picasaweb.google") > 0):
                ua = urllib.urlencode({'iagent' : UASTR})
                vidcontent=postContent("http://cache.dldrama.com/gk/43/plugins_player.php",ua+"&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",domain)
                vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
                hdmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?)').findall(vidmatch[-1][2])
                if(len(hdmatch) > 0):
                    vidmatch=hdmatch
                vidlink=vidmatch[-1][0]
           elif (newlink.find("docs.google.com") > -1):
                vidcontent = GetContent(newlink)
                vidmatch=re.compile('"url_encoded_fmt_stream_map":"(.+?)",').findall(vidcontent)
                if(len(vidmatch) > 0):
                        vidparam=urllib.unquote_plus(vidmatch[0]).replace("\u003d","=")
                        vidlink=re.compile('url=(.+?)\u00').findall(vidparam)
           elif (newlink.find("allmyvideos") > -1):
                videoid=  re.compile('http://allmyvideos.net/embed-(.+?).html').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://allmyvideos.net/"+videoid[0]
                link = GetContent(newlink)
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent2(newlink,posdata,url)
                vidlink=re.compile('"file" : "(.+?)",').findall(pcontent)[0]
           elif (newlink.find("nosvideo") > -1):
                videoid=  re.compile('http://nosvideo.com/embed/(.+?)/').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://nosvideo.com/"+videoid[0]
                link = GetContent(newlink)
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"rand":"","id":idkey,"referer":url,"method_free":"Continue+to+Video","method_premium":"","down_script":"1"})
                pcontent=postContent2(newlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div name="placeholder" id="placeholder">(.+?)</div></div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                xmlUrl=re.compile('"playlist=(.+?)&').findall(unpacked)[0]
                vidcontent = postContent2(xmlUrl,None,url)
                vidlink=re.compile('<file>(.+?)</file>').findall(vidcontent)[0]
           elif (newlink.find("uploadpluz") > -1):
                videoid=  re.compile('http://nosvideo.com/embed/(.+?)/').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://nosvideo.com/"+videoid[0]
                link = GetContent(newlink)
                pcontent=''.join(link.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1].replace('<script type="text/javascript">',"")
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                vidUrl=re.compile('"file","(.+?)"').findall(unpacked)[0]
                vidlink=vidUrl+"|Referer=http%3A%2F%2Fuploadpluz.com%3A8080%2Fplayer%2Fplayer.swf"
           elif (newlink.find("yourupload") > -1):
                link = GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                vidlink=re.compile('<a class="btn btn-primary" [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                vidlink=vidlink.replace("download.yucache.net","stream.yucache.net")
           elif (newlink.find("nowvideo") > -1):
                link = GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)
                if(len(codeid) > 0):
                     codeid=codeid[0]
                else:
                     codeid=""
                keycode=re.compile('flashvars.filekey=(.+?);').findall(link)[0]
                keycode=re.compile('var\s*'+keycode+'="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.nowvideo.sx/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
           elif (newlink.find("180upload") > -1):
                if(newlink.find("embed") == -1):
                      vidcode = re.compile('180upload.com/(.+?)dk').findall(newlink+"dk")[0] 
                      newlink= 'http://180upload.com/embed-'+vidcode+'.html'
                link=GetContent(newlink)
                file_code = re.compile('<input type="hidden" name="file_code" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_width = re.compile('<input type="hidden" name="embed_width" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_height = re.compile('<input type="hidden" name="embed_height" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                test34 = re.compile('<input type="hidden" name="nwknj3" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"file_code":file_code,"referer":url,"embed_width":embed_width,"embed_height":embed_height,"nwknj3":test34})
                pcontent=postContent2(newlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                unpacked=unpacked.replace("\\","")
                vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(unpacked)[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("playlists") > -1):
                playlistid=re.compile('playlists/(.+?)\?v').findall(newlink)
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("list=") > -1):
                playlistid=re.compile('videoseries\?list=(.+?)&').findall(newlink+"&")
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("/p/") > -1):
                playlistid=re.compile('/p/(.+?)\?').findall(newlink)
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("/embed/") > -1):
                playlistid=re.compile('/embed/(.+?)\?').findall(newlink+"?")
                vidlink=getYoutube(playlistid[0])
           elif (newlink.find("youtube") > -1):
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                print "in youtube" + lastmatch[0]
                vidlink=getYoutube(lastmatch[0])
           else:
                #import urlresolver
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + url
                if source:
                        vidlink = source.resolve()
                else:
                        vidlink =""
           return vidlink
		   
def extractFlashVars(data):
    for line in data.split("\n"):
            index = line.find("ytplayer.config =")
            if index != -1:
                found = True
                p1 = line.find("=", (index-3))
                p2 = line.rfind(";")
                if p1 <= 0 or p2 <= 0:
                        continue
                data = line[p1 + 1:p2]
                break
    if found:
            data=data.split(";(function()",1)[0]
            data = json.loads(data)
            flashvars = data["args"]
    return flashvars    
		
def selectVideoQuality(links):
        link = links.get
        video_url = ""
        fmt_value = {
                5: "240p h263 flv container",
                18: "360p h264 mp4 container | 270 for rtmpe?",
                22: "720p h264 mp4 container",
                26: "???",
                33: "???",
                34: "360p h264 flv container",
                35: "480p h264 flv container",
                37: "1080p h264 mp4 container",
                38: "720p vp8 webm container",
                43: "360p h264 flv container",
                44: "480p vp8 webm container",
                45: "720p vp8 webm container",
                46: "520p vp8 webm stereo",
                59: "480 for rtmpe",
                78: "seems to be around 400 for rtmpe",
                82: "360p h264 stereo",
                83: "240p h264 stereo",
                84: "720p h264 stereo",
                85: "520p h264 stereo",
                100: "360p vp8 webm stereo",
                101: "480p vp8 webm stereo",
                102: "720p vp8 webm stereo",
                120: "hd720",
                121: "hd1080"
        }
        hd_quality = 1

        # SD videos are default, but we go for the highest res
        #print video_url
        if (link(35)):
            video_url = link(35)
        elif (link(59)):
            video_url = link(59)
        elif link(44):
            video_url = link(44)
        elif (link(78)):
            video_url = link(78)
        elif (link(34)):
            video_url = link(34)
        elif (link(43)):
            video_url = link(43)
        elif (link(26)):
            video_url = link(26)
        elif (link(18)):
            video_url = link(18)
        elif (link(33)):
            video_url = link(33)
        elif (link(5)):
            video_url = link(5)

        if hd_quality > 1:  # <-- 720p
            if (link(22)):
                video_url = link(22)
            elif (link(45)):
                video_url = link(45)
            elif link(120):
                video_url = link(120)
        if hd_quality > 2:
            if (link(37)):
                video_url = link(37)
            elif link(121):
                video_url = link(121)

        if link(38) and False:
            video_url = link(38)
        for fmt_key in links.iterkeys():

            if link(int(fmt_key)):
                    text = repr(fmt_key) + " - "
                    if fmt_key in fmt_value:
                        text += fmt_value[fmt_key]
                    else:
                        text += "Unknown"

                    if (link(int(fmt_key)) == video_url):
                        text += "*"
            else:
                    print "- Missing fmt_value: " + repr(fmt_key)

        video_url += " | " + UASTR


        return video_url

def getYoutube(videoid):

                code = videoid
                linkImage = 'http://i.ytimg.com/vi/'+code+'/default.jpg'
                req = urllib2.Request('http://www.youtube.com/watch?v='+code+'&fmt=18')
                req.add_header('User-Agent', UASTR)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                if len(re.compile('shortlink" href="http://youtu.be/(.+?)"').findall(link)) == 0:
                        if len(re.compile('\'VIDEO_ID\': "(.+?)"').findall(link)) == 0:
                                req = urllib2.Request('http://www.youtube.com/get_video_info?video_id='+code+'&asv=3&el=detailpage&hl=en_US')
                                req.add_header('User-Agent', UASTR)
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                
                flashvars = extractFlashVars(link)

                links = {}

                for url_desc in flashvars[u"url_encoded_fmt_stream_map"].split(u","):
                        url_desc_map = cgi.parse_qs(url_desc)
                        if not (url_desc_map.has_key(u"url") or url_desc_map.has_key(u"stream")):
                                continue

                        key = int(url_desc_map[u"itag"][0])
                        url = u""
                        if url_desc_map.has_key(u"url"):
                                url = urllib.unquote(url_desc_map[u"url"][0])
                        elif url_desc_map.has_key(u"stream"):
                                url = urllib.unquote(url_desc_map[u"stream"][0])

                        if url_desc_map.has_key(u"sig"):
                                url = url + u"&signature=" + url_desc_map[u"sig"][0]
                        links[key] = url
                highResoVid=selectVideoQuality(links)
                return highResoVid  

def ParseVideoLink(url,name,movieinfo):
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving video Link...')       
    dialog.update(0)
    if movieinfo=="direct":
		return url
    link =GetContent(url)
    link = ''.join(link.splitlines()).replace('\'','"')
    # borrow from 1channel requires you to have 1channel
    win = xbmcgui.Window(10000)
    win.setProperty('1ch.playing.title', movieinfo)
    win.setProperty('1ch.playing.season', str(3))
    win.setProperty('1ch.playing.episode', str(4))
    # end 1channel code
    #redirlink=url
    try:
        redirlink = urllib.unquote(url.encode('utf-8'))
    except: pass
    try:
    #if True:
        if (redirlink.find("youtube") > -1):
                vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(redirlink)
                vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
                vidlink='plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+vidlink
        elif (redirlink.find("videoting") > -1):
                media_url= ""
                media_url = re.compile('player.src\(\[{src:\s*"(.+?)",').findall(link)[0]
                vidlink = media_url
        elif (redirlink.find("vidxtreme") > -1):
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(link)
                if(len(paccked) > 0):
					pcontent=jsunpack.unpack(paccked[0].replace('"','\''))
					mediacontent = re.compile('sources:\[(.+?)\]').findall(pcontent)[0]
					formatjson= "["+mediacontent.replace("file:","'file':").replace("label:","'label':")+"]"
					mediaurl=json.loads(formatjson.replace("'",'"'))
                vidlink = mediaurl[-1]["file"]
        elif (redirlink.find(".me/embed") > -1 or redirlink.find(".net/embed") > -1 or redirlink.find(".me/gogo") > -1 or redirlink.find("embed.php?") > -1):
                media_url= ""
                media_url = re.compile('_url\s*=\s*"(.+?)";').findall(link)[0]
                vidlink = urllib.unquote_plus(media_url) #GetDirVideoUrl(media_url)
        elif (redirlink.find("yourupload") > -1 or redirlink.find("oose.io") > -1):
                media_url= ""
                media_url = re.compile('<meta property="og:video" [^>]*content=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                vidlink = media_url
        elif (redirlink.find("video44") > -1):
                media_url= ""
                media_url = re.compile('file:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
                     media_url = re.compile('url:\s*"(.+?)"').findall(link)
                vidlink = media_url[0]
        elif (redirlink.find("videobug") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)
                if(len(media_url)==0):
					media_url = re.compile('hd:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
					media_url = re.compile('sdm:\s*"(.+?)"').findall(link)
                vidlink = urllib.unquote(media_url[0])
        elif (redirlink.find("play44") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("byzoo") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("vidzur") > -1 or redirlink.find("videofun") > -1 or redirlink.find("auengine") > -1):
                media_url= ""
                op = re.compile('playlist:\s*\[(.+?)\]').findall(link)[0]
                urls=op.split("{")
                for rows in urls:
                     if(rows.find("url") > -1):
                          murl= re.compile('url:\s*"(.+?)"').findall(rows)[0]
                          media_url=urllib.unquote_plus(murl)
                vidlink = media_url
        elif (redirlink.find("cheesestream") > -1 or redirlink.find("yucache") > -1):
                vidlink = re.compile('<meta property="og:video" content="(.+?)"/>').findall(link)[0]
        elif (redirlink.find("video.google.com") > -1):
                match=redirlink.split("docid=")
                glink=""
                newlink=redirlink+"&dk"
                if(len(match) > 0):
                        glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[1].split("&")[0])
                else:
                        match=re.compile('http://video.google.com/googleplayer.swf.+?docId=(.+?)&dk').findall(newlink)
                        if(len(match) > 0):
                                glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                gcontent=re.compile('<div class="mod_download"><a href="(.+?)" title="Click to Download">').findall(glink)
                if(len(gcontent) > 0):
                        vidlink=gcontent[0]
                else:
                        vidlink=""
        elif (redirlink.find("movshare") > -1):
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)[0]
                keycode=re.compile('flashvars.filekey="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.movshare.net/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
        elif (redirlink.find("nowvideo") > -1):
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)[0]
                keycode=re.compile('flashvars.filekey=(.+?);').findall(link)[0]
                keycode=re.compile('var\s*'+keycode+'="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.nowvideo.sx/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
        elif (redirlink.find("bestreams") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 2)
                dialog.create('Resolving', 'Resolving bestreams Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("vidx") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 10)
                dialog.create('Resolving', 'Resolving vidx Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Weiter+%2F+continue",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("streamin") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving streamin Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                tmplink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*streamer:\s*"(.+?)"').findall(pcontent)
                vidlink = tmplink[0][1]+"/"+tmplink[0][0] + " playPath="+tmplink[0][0]
                if(tmplink[0][0].find("http:") > -1):
                        #vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                        vidlink = tmplink[0][0]
        elif (redirlink.find("slickvid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving slickvid Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Watch",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("vidpaid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 1)
                dialog.create('Resolving', 'Resolving vidpaid Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Continue+to+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("uploadnetwork") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('"file":\s*"(.+?)"').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("divxpress") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)
                if(len(packed) == 0):
                      packed = re.compile('<div id="player_code"><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                      sUnpacked = unpackjs4(packed).replace("\\","")
                      vidlink = re.compile('src="(.+?)"').findall(sUnpacked)[0]
                else:
                      packed=packed[0]
                      sUnpacked = unpackjs4(packed).replace("\\","")
                      vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(sUnpacked)

        elif (redirlink.find("videopremium") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"referer":"","method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('src="/swfobject.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                sUnpacked = unpackjs4(packed)  
                vidpart = re.compile('"file":"(.+?)",p2pkey:"(.+?)"').findall(sUnpacked)[0]
                vidswf = re.compile('embedSWF\("(.+?)",').findall(sUnpacked)[0]
                vidlink=""
                if(len(vidpart) > 0):
                        vidlink = "rtmp://e9.md.iplay.md/play/"+vidpart[1]+" swfUrl="+vidswf+" playPath="+vidpart[1] +" pageUrl=" + redirlink + " tcUrl=rtmp://e9.md.iplay.md/play"
                #vidlink="rtmp://e9.md.iplay.md/play/mp4:rx90tddtnfmc.f4v swfUrl=http://videopremium.tv/uplayer/uppod.swf pageUrl=http://videopremium.tv/rx90tddtnfmc playPath=mp4:rx90tddtnfmc.f4v tcUrl=rtmp://e9.md.iplay.md/play"
        elif (redirlink.find("faststream") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving faststream Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Continue+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("videomega") > -1):
                refkey= re.compile('\?ref=(.+?)&dk').findall(redirlink+"&dk")[0]
                vidcontent="http://videomega.tv/iframe.php?ref="+refkey
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('if\s*\(!validstr\){\s*document.write\(unescape\("(.+?)"\)\);\s*}').findall(pcontent)[0]
                vidcontent=urllib.unquote_plus(urlcode)
                vidlink = re.compile('file:\s*"(.+?)",').findall(vidcontent)[0]
        elif (redirlink.find("v-vids") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("thefile") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('<span>\s*<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>\s*</span>').findall(pcontent)[0][0]
        elif (redirlink.find("topvideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('jwplayer.key="(.+?)";</script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0][1]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("gamovideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving gamovideo Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/jwplayer.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("vodlocker") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving bestreams Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = ""
                vidlink2 = re.compile('setup\(\{\s*file: "(.+?)",\s*streamer: "(.+?)",\s*').findall(pcontent)
                if(len(vidlink2) > 0):
                        vidlink = vidlink2[0][1]+"/mp4:"+vidlink2[0][0]+" swfUrl=http://vodlocker.com/player/player.swf playPath=mp4:"+vidlink2[0][0]
        elif (redirlink.find("exashare") > -1):
                packed = re.compile('/jwplayer.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(link)[0]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("sharesix") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url})
                pcontent=postContent(redirlink,posdata+"&method_free=Free",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('swfobject.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('.addVariable\("file",\s*"(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("bonanzashare") > -1):
                capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(link)
                capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                capstring =""
                for tmp,aph in capchar:
                        capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":"","rand":rand,"method_premium":"","code":capstring,"down_direct":ddirect})
                newpcontent=postContent(redirlink,posdata,url)
                newpcontent=''.join(newpcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Download the file</a>').findall(newpcontent)[0] 
        elif (redirlink.find("videozed") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free"  value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,strdomain)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(pcontent)
                capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                capstring =""
                for tmp,aph in capchar:
                        capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))

                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(pcontent)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(pcontent)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(pcontent)[0]
                rand = re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(pcontent)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(pcontent)[0]
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":mfree,"rand":rand,"method_premium":"","code":capstring,"down_direct":ddirect})
                newpcontent=postContent(redirlink,posdata,url)
                newpcontent=''.join(newpcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(newpcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidsrc = re.compile('src="(.+?)"').findall(unpacked)
                if(len(vidsrc) == 0):
                         vidsrc=re.compile('"file","(.+?)"').findall(unpacked)
                vidlink=vidsrc[0]
        elif (redirlink.find("donevideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('action=""><input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free"  value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('src="(.+?)"').findall(unpacked)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(unpacked)
                vidlink=vidlink[0]
        elif (redirlink.find("clicktovie") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                capchacon =re.compile('another captcha</a>(.+?)</script>').findall(pcontent)[0]
                capchalink=re.compile('<script type="text/javascript" src="(.+?)">').findall(capchacon)
                strCodeInput="recaptcha_response_field"
                respfield=""
                if(len(capchalink)==0):
                         capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(pcontent)
                         capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                         capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                         capstring =""
                         for tmp,aph in capchar:
                                  capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))
                         puzzle=capstring
                         strCodeInput="code"
                else:
                         imgcontent=GetContent(capchalink[0])
                         respfield=re.compile("challenge : '(.+?)'").findall(imgcontent)[0]
                         imgurl="http://www.google.com/recaptcha/api/image?c="+respfield
                         solver = InputWindow(captcha=imgurl)
                         puzzle = solver.get()
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(pcontent)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(pcontent)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(pcontent)[0]
                rand = re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(pcontent)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(pcontent)[0]
                #replace codevalue with capture screen
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":mfree,"rand":rand,"method_premium":"","recaptcha_challenge_field":respfield,strCodeInput:puzzle,"down_direct":ddirect})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.split("</script>")[1]
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('"file","(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("vidbull") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving vidbull Link...') 
                dialog.update(50)
                pcontent=postContent2(redirlink,posdata,url)
                #pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink= re.compile('<!--RAM disable direct link<a href="(.+?)" target="_top">').findall(pcontent)
                if(len(vidlink) > 0):
                         filename = vidlink[0].split("/")[-1:][0]
                         vidlink=vidlink[0].replace(filename,"video.mp4")
                else:
                         sPattern =  '<script type=(?:"|\')text/javascript(?:"|\')>eval\(function\(p,a,c,k,e,[dr]\)(?!.+player_ads.+).+?</script>'
                         r = re.search(sPattern, pcontent, re.DOTALL + re.IGNORECASE)
                         if r:
                              sJavascript = r.group()
                              sUnpacked = jsunpack.unpack(sJavascript)
                              stream_url = re.search('[^\w\.]file[\"\']?\s*[:,]\s*[\"\']([^\"\']+)', sUnpacked)
                              if stream_url:
                                    vidlink= stream_url.group(1)

        elif (redirlink.find("nosvideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"rand":"","id":idkey,"referer":url,"method_free":"Continue+to+Video","method_premium":"","down_script":"1"})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div name="placeholder" id="placeholder">(.+?)</div></div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                xmlUrl=re.compile('"playlist=(.+?)&').findall(unpacked)[0]
                vidcontent = postContent2(xmlUrl,None,url)
                vidlink=re.compile('<file>(.+?)</file>').findall(vidcontent)[0]

        elif (redirlink.find("flashx.tv") > -1):
                idkey = re.compile('<input name="objectid" id="objectid" type="hidden" value="(.+?)" />').findall(link)[0]
                ebmurl="http://play.flashx.tv/player/embed.php?vid="+idkey
                plycontent=GetContent(ebmurl)
                plycontent= ''.join(plycontent.splitlines()).replace('\'','"')
                yes = re.compile('<input name="yes" type="hidden" value="(.+?)">').findall(plycontent)[0]
                sec = re.compile('<input name="sec" type="hidden" value="(.+?)">').findall(plycontent)[0]
                posdata=urllib.urlencode({"yes":yes,"sec":sec})
                plycontent=postContent2("http://play.flashx.tv/player/playfx.php",posdata,ebmurl)
                plycontent= ''.join(plycontent.splitlines()).replace('\'','"')
                playercode=re.compile('<object [^>]*data=["\']?([^>^"^\']+)["\']?[^>]*>').findall(plycontent)[0]
                playercode=playercode.split("config=")[1]
                finalcontent=GetContent(playercode)
                vidlink=re.compile('<file>(.+?)</file>').findall(finalcontent)
                if(len(vidlink)==0):
                      finalcontent=GetContent(playercode)
                      vidlink=re.compile('<file>(.+?)</file>').findall(finalcontent)[0]
                else:
                      vidlink=vidlink[0]
        elif (redirlink.find("speedvid") > -1):
                keycode=re.compile('\|image\|(.+?)\|(.+?)\|file\|').findall(link)
                domainurl=re.compile('\[IMG\](.+?)\[/IMG\]').findall(link)[0]
                domainurl=domainurl.split("/i/")[0]
                vidlink=domainurl+"/"+keycode[0][1]+"/v."+keycode[0][0]
        elif (redirlink.find("vreer") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)" />').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)" />').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)" />').findall(link)[0]
                rand = re.compile('<input type="hidden" name="hash" value="(.+?)" />').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"hash":rand,"id":idkey,"referer":"","method_free":"Free Download"})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 20)
                dialog.create('Resolving', 'Resolving vreer Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('file: "(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("allmyvideos") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent2(redirlink,posdata,url)
                packed = get_match( pcontent , "(<script type='text/javascript'>eval\(.*?function\(p,\s*a,\s*c,\s*k,\s*e,\s*d.*?)</script>",1)
                unpacked = unpackjs(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                try:
                    vidlink = get_match(unpacked,"'file'\s*\:\s*'([^']+)'")+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
                except:
                    vidlink = get_match(unpacked,'"file"\s*\:\s*"([^"]+)"')+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )

        elif (redirlink.find("cyberlocker") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('action=""><input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":"Free Download"})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('name="src"value="(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("promptfile") > -1):
                chash = re.compile('<input type="hidden" name="chash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"chash":chash})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Download File</a>').findall(pcontent)[0]
        elif (redirlink.find("veervid") > -1):
                posturl=re.compile('<form action="(.+?)" method="post">').findall(link)[0]
                pcontent=postContent(posturl,"continue+to+video=Continue+to+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('so.addVariable\("file","(.+?)"').findall(pcontent)[0]
        elif (redirlink.find("sharerepo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname.encode('utf-8'),"id":idkey,"referer":url,"method_free":"Free Download","down_direct":ddirect})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed=packed.split("</script>")[1]
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('"file","(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("nowdownloa") > -1):
                ddlpage = re.compile('<a class="btn btn-danger" href="(.+?)">Download your file !</a>').findall(link)[0]
                mainurl = redirlink.split("/dl/")[0]
                ddlpage= mainurl+ddlpage
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 30)
                dialog.create('Resolving', 'Resolving nowdownloads Link...') 
                dialog.update(50)
                pcontent=GetContent(ddlpage)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                linkcontent =re.compile('Slow download</span>(.+?)</div>').findall(pcontent)[0]
                vidlink = re.compile('<a href="(.+?)" class="btn btn-success">').findall(linkcontent)[0]
        elif (redirlink.find("youwatch") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                rand = re.compile('<input type="hidden" name="hash" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"hash":rand,"id":idkey,"referer":"","imhuman":"Slow Download","method_premium":""})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 10)
                dialog.create('Resolving', 'Resolving youwatch Link...') 
                dialog.update(50)
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines())
                packed = re.compile("<span id='flvplayer'></span>(.+?)</script>").findall(pcontent)[0]
                unpacked = unpackjs5(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("videoslasher") > -1):
                user=re.compile('user: ([^"]+),').findall(link)[0]
                code=re.compile('code: "([^"]+)",').findall(link)[0]
                hash1=re.compile('hash: "([^"]+)"').findall(link)[0]
                formdata = { "user" : user, "code": code, "hash" : hash1}
                data_encoded = urllib.urlencode(formdata)
                request = urllib2.Request('http://www.videoslasher.com/service/player/on-start', data_encoded) 
                response = urllib2.urlopen(request)
                ccontent = response.read()
                ckStr = cj['.videoslasher.com']['/']['authsid'].name+'='+cj['.videoslasher.com']['/']['authsid'].value
                playlisturl = re.compile('playlist: "(.+?)",').findall(link)[0]
                playlisturl = redirlink.split("/video/")[0]+playlisturl
                pcontent=postContent2(playlisturl,"",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink= re.compile(':content url="([^"]+)" type="video/x-flv" [^>]*>').findall(pcontent)[0]
                vidlink= ( '%s|Cookie="%s"' % (vidlink,ckStr) )
        #elif (redirlink.find("billionuploads") > -1):
        #        vidlink=resolve_billionuploads(redirlink,tmpcontent)
        #elif (redirlink.find("movreel") > -1):
        #        vidlink=resolve_movreel(redirlink,tmpcontent)
        elif (redirlink.find("jumbofiles") > -1):
                vidlink=resolve_jumbofiles(redirlink,tmpcontent)
        elif (redirlink.find("glumbouploads") > -1):
                vidlink=resolve_glumbouploads(redirlink,tmpcontent)
        elif (redirlink.find("sharebees") > -1):
                vidlink=resolve_sharebees(redirlink,tmpcontent)
        elif (redirlink.find("uploadorb") > -1):
                vidlink=resolve_uploadorb(redirlink,tmpcontent)
        elif (redirlink.find("vidhog") > -1):
                vidlink=resolve_vidhog(redirlink,tmpcontent)
        elif (redirlink.find("speedyshare") > -1):
                vidlink=resolve_speedyshare(redirlink,tmpcontent)
        elif (redirlink.find("180upload") > -1):
                vidcode = re.compile('180upload.com/(.+?)dk').findall(redirlink+"dk")[0] 
                urlnew= 'http://180upload.com/embed-'+vidcode+'.html'
                link=GetContent(urlnew)
                file_code = re.compile('<input type="hidden" name="file_code" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_width = re.compile('<input type="hidden" name="embed_width" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_height = re.compile('<input type="hidden" name="embed_height" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                test34 = re.compile('<input type="hidden" name="test34" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"file_code":file_code,"referer":url,"embed_width":embed_width,"embed_height":embed_height,"test34":test34})
                pcontent=postContent2(urlnew,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                unpacked=unpacked.replace("\\","")
                vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(unpacked)[0]
				
        else:
                if(redirlink.find("putlocker.com") > -1 or redirlink.find("sockshare.com") > -1):
                        redir = redirlink.split("/file/")
                        redirlink = redir[0] +"/file/" + redir[1].upper()
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + redirlink
                if source:
                        vidlink = source.resolve()

    except:
                if(redirlink.find("putlocker.com") > -1 or redirlink.find("sockshare.com") > -1):
                        redir = redirlink.split("/file/")
                        redirlink = redir[0] +"/file/" + redir[1].upper()
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + redirlink
                if source:
                        vidlink = source.resolve()
    dialog.close()
    return vidlink

				
def loadVideos(url,name):
                GA("LoadVideo","NA")
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!, Loading video link into XBMC Media Player,5000)")
                try:
                    url = urllib.unquote(url.encode('utf-8'))
                except: pass
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
                try:
                    req = urllib2.Request(url, headers=hdr)
                    response = urllib2.urlopen(req)
                    link=response.read()
                    response.close()
                except: link = GetContent(url)
                
                try:
                    link = link.encode("UTF-8")
                except: pass
		newlink = ''.join(link.splitlines()).replace('\t','').replace('amp;','')
		try:
			newlink =newlink.encode("UTF-8")
		except: pass
		#match=re.compile('<input type="hidden" id="linkPlayer" value="(.+?)" />').findall(newlink)
		match=re.compile('<video id="player" [^>]*>\s*<source src="(.+?)" [^>]*>').findall(newlink)
##		print ("============================ POSTING match ============================")
##		print match
		match2=re.compile('<IFRAME id="player" src="(.+?)" [^>]*>').findall(newlink)
##		print ("============================ POSTING match2 ============================")
##		print match2
		#ParseVideoLink(match,name,"")
		#vidlink=Videosresolve(match[0],name)
		if(len(match) > 0):
                    vidlink = match[0]
                elif(len(match2) > 0):
                    vidlink = match2[0]
                else:
                    vidlink = ""
##		print ("============================ POSTING vidlink ============================")
##		print vidlink
                redirlink = vidlink
                if(redirlink.find("googlevideo.com") > 0):
                    vidlink = urllib.unquote(vidlink)
                    Videosresolve(vidlink,name)
                    addDir2("GoogleVideo | Unknown Quality",vidlink,8,"")
		elif(redirlink.find("openload.co") > 0):
##                    sources = []
##                    label=name
##                    hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
##                    sources.append(hosted_media)
##                    source = urlresolver.choose_source(sources)
##                    print "inresolver=" + url
##                    if source:
##                            newvidlink = source.resolve()
##                    else:
##                            newvidlink =""
                    
##                    Videosresolve(vidlink,name)
                    addDir2("OpenLoad | Unknown Quality",redirlink,13,"")

		elif(redirlink.find("vk.com") > 0):

                    addDir2("vk.com | Unknown Quality",redirlink,13,"")
                    
		elif(redirlink.find("ok.ru") > 0):
                    oklink = okru_streams(vidlink,redirlink)
                    print ("============================ POSTING oklink sources ============================")
                    print oklink
                    
                    labels = []
                    
                    for item in oklink:
                            labels.append(item['name'])
                    
                    dialog = xbmcgui.Dialog()
                    
                    index = dialog.select('Select video source', labels)
                    if index > -1:
                            playStream(oklink[index]['url'], "", "")
                    else:
                            return

                else:
                    if vidlink != "":
                        addDir2("Googlecontent | Unknown Quality",vidlink,8,"")

def playStream(url,title,thumbnail):
        print ("============================ POSTING oklink url ============================")
        print url
        win = xbmcgui.Window(10000)
        win.setProperty('hdfree.playing.title', title.lower())
        
        item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        item.setInfo(type = "Video", infoLabels = {"title": title})
        
        xbmc.Player().play(item=url, listitem=item)
        
        return True

def _okru_to_res(string):
    string = string.strip()
    resolution = string
    if string == 'full':
        resolution = 'Ok.ru | 1080p'
    elif string == 'hd':
        resolution = 'Ok.ru | 720p'
    elif string == 'sd':
        resolution = 'Ok.ru | 480p'
    elif string == 'low':
        resolution = 'Ok.ru | 360p'
    elif string == 'lowest':
        resolution = 'Ok.ru | 240p'
    elif string == 'mobile':
        resolution = 'Ok.ru | 144p'

    return resolution


def okru_streams(url,redirlink):
##    HEADERS = {
##        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
##        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
##    }

    URL = {}
    URL['base']	= redirlink

    id = re.search('\d+', url).group(0)
    jsonUrl = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=' + id
    jsonSource = json.loads(http_req(jsonUrl))

    sources = []
    for source in jsonSource['videos']:
        name = _okru_to_res(source['name'])
        link = '%s|User-Agent=%s&Accept=%s&Referer=%s'
        link = link % (source['url'], HEADERS['User-Agent'], HEADERS['Accept'], urllib.quote_plus(URL['base']))
        item = {'name': name, 'url': link}
        sources.append(item)
        
##        addDir2(name,link,8,"")
        
    print ("============================ POSTING okru sources ============================")
    print sources

    return sources

def http_req(url, getCookie=False, data=None, customHeader=None):
        if data: data = urllib.urlencode(data)
        if customHeader:
                req = urllib2.Request(url, data, customHeader)
        req = urllib2.Request(url, data, HEADERS)
        response = urllib2.urlopen(req)
        source = response.read()
        response.close()
        if getCookie:
                cookie = response.headers.get('Set-Cookie')
                return {'source': source, 'cookie': cookie}
        return source

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
        try:
            xbmcPlayer.play(vidlink)
        except:
            d = xbmcgui.Dialog()
            d.ok(url,"Letters for captcha incorrect",'Try again')
		
def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():
    if GA_PRIVACY == True:
        return
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
    if GA_PRIVACY == True:
        return
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':UASTR}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        if GA_PRIVACY == True:
            return
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
        if versionNumber > 13:
			logname="kodi.log"
        else:
			logname="xbmc.log"
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
                log = os.path.join(log_path, logname)
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, logname)
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, logname)
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
##        name = cleanName(name)
##        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))+"&mirrorname="+urllib.quote_plus(mirrorname)
##        ok=True
##        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
##        liz.setInfo( type="Video", infoLabels={ "Title": name } )
##        contextMenuItems = []
##        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
##        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
##        return ok

        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&movieinfo="+urllib.quote_plus(movieinfo)
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
        name = cleanName(name)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage):
        name = cleanName(name)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def cleanName(name):
        strireplace = re.compile(re.escape('Watch Online '), re.IGNORECASE)
        return strireplace.sub('',name)

def cleanPage(name):
        strireplace = re.compile(re.escape(' '), re.IGNORECASE)
        name = strireplace.sub('',name)
        strireplace = re.compile(re.escape('&quot;'), re.IGNORECASE)
        name = strireplace.sub('"',name)
        return name
        
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
elif mode==12:
       GA("INDEX2",name)      
       INDEX2(url)
elif mode==13:
       ResolveUrl(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
