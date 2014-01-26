# -*- coding: cp1252 -*-
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
VERSION = "1.0.10" #<---- PLUGIN VERSION
#domainlist = [" ", " ", " "]
#domain = domainlist[int(ADDON.getSetting('domainurl'))]
def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        #addDir('Search',' ',4,' ')
        addDir('Recent Episodes','http://tvbdo.com',14,'')
        addDir('TVB Dramas','http://tvbdo.com/hong-kong-drama',2,'')
        #addDir('HK Movies','http://www.tvbdo.com/category/movies/',14,'')
        addDir('HK Variety Shows','http://www.tvbdo.com/category/hk-variety/',2,'')
        #addDir('HK On-Going Variety Shows','http://www.tvbdo.com/category/on-going-variety-shows/',2,'')
        #addDir('HKTV','http://www.tvbdo.com/category/hktv/',2,'')
        addDir('Mainland Dramas','http://tvbdo.com/shows/country/china',2,'')
        addDir('Taiwan Dramas','http://tvbdo.com/shows/country/taiwan',2,'')
        addDir('Movies','http://tvbdo.com/movies',2,'')

def INDEX(url,newmode):
    #try:
        try:
            url = urllib.unquote(url.encode('utf-8'))
        except: pass
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        try:
            link=response.read()
            response.close()
        except: link = GetContent(url)
        
        try:
            link = link.encode("UTF-8")
        except: pass

        vidmode=18
        
        if(newmode==13):
                vidmode=10
        elif(newmode==14):
                vidmode=11
        
        newlink = ''.join(link.splitlines()).replace('\t','').replace('\'','"').replace('&#8217;','\'').replace('http://tvbdo.com','http://www.tvbdo.com')
        listcontent=re.compile('<div id="main">(.+?)</body>').findall(newlink)

        print "============================ POSTING listcontent ============================"
        print (listcontent)
        
        if(newmode==14):
            match=re.compile('<li>[^>]*<a href="(.+?)"[^>]*>(.+?)</a>').findall(listcontent[0])

            for (vurl,vname) in match:
                vname = vname.replace('&#8211;','-').replace('&#8217;','\'')
                try:
                    addDir(vname,url_fix(vurl),15,"")
                except:
                    addDir(vname.decode("utf-8"),url_fix(vurl),15,"")
            
        else:
            match=re.compile('<img src="(.+?)"[^>]*>(.+?)<h2[^>]*>[^>]*<a href="(.+?)"[^>]*>(.+?)</a>[^>]*</h2>').findall(listcontent[0])
            
            for (vimg,vtmp,vurl,vname) in match:
                vname = vname.replace('&#8211;','-')
                try:
                      addDir(vname,url_fix(vurl),vidmode,vimg)
                except:
                      addDir(vname.decode("utf-8"),url_fix(vurl),vidmode,vimg)
                  
        pagecontent=re.compile('<div class="loop-nav-inner">(.+?)</div>').findall(newlink)

        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)" [^>]*>(.+?)</a>').findall(pagecontent[0])
                for (vurl,vname) in match5:
                    vname = vname.replace('&laquo;','<<').replace('&raquo;','>>')
                    try:
                        addDir('[COLOR yellow]page: [/COLOR]' + vname,vurl,2,'')
                    except:
                        addDir('[COLOR yellow]page: [/COLOR]' + vname.decode('utf-8'),vurl,2,'')
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
##        print ("============================ POSTING url ============================")
##        print (url)        
##        try:
##            url = urllib.unquote(url.encode('utf-8'))
##        except: pass
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        try:
            link=response.read()
            response.close()
        except: link = GetContent(url)

        link = ''.join(link.splitlines()).replace('\'','"').replace('\t','').replace('\\','')
##        print ("============================ POSTING abclink ============================")
##        print link

        partlist=re.compile('function chsplayer(.+?)\}\)').findall(urllib.unquote(link).decode('utf-8'))
        partlist2=re.compile('function engplayer(.+?)\}\)').findall(urllib.unquote(link).decode('utf-8'))
        engsubsNone=re.compile('eng2222 \{[^>]*display: none').findall(urllib.unquote(link).decode('utf-8'))
        #altpartlist=re.compile('var parts =(.+?)</iframe>').findall(urllib.unquote(link).decode('utf-8'))

        if(len(partlist)<1):
            altpartlist=re.compile('Source 1(.+?)Source 1').findall(urllib.unquote(link).decode('utf-8'))
##            print ("============================ POSTING altpartlist ============================")
##            print (altpartlist)

            if(altpartlist):
                altpartlistlink=re.compile('href="(.+?)"').findall(altpartlist[0])
##                print ("============================ POSTING altpartlistlink ============================")
##                print (altpartlistlink)
                for vlink in altpartlistlink:
                    altParts(vlink,name)

            altpartlist2=re.compile('Source 1 Chinese</b></span><iframe width=(.+?)>').findall(urllib.unquote(link).decode('utf-8'))
##            print ("============================ POSTING altpartlist2 ============================")
##            print (altpartlist2)

            if(altpartlist2):
                altpartlistlink2=re.compile('src="(.+?)"').findall(altpartlist2[0])
##                print ("============================ POSTING altpartlistlink2 ============================")
##                print (altpartlistlink2)
                for vlink in altpartlistlink2:
                    videomega(vlink,name)

            altpartlist3=re.compile('Source 1 English</b></span><iframe width=(.+?)>').findall(urllib.unquote(link).decode('utf-8'))
##            print ("============================ POSTING altpartlist3 ============================")
##            print (altpartlist3)

            if(altpartlist3):
                altpartlistlink3=re.compile('src="(.+?)"').findall(altpartlist3[0])
##                print ("============================ POSTING altpartlistlink2 ============================")
##                print (altpartlistlink3)
                for vlink in altpartlistlink3:
                    name = name + ' (English subs)'
                    videomega(vlink,name)

            altpartlist4=re.compile('Source 1 LQ</b></span><iframe width=(.+?)>').findall(urllib.unquote(link).decode('utf-8'))
##            print ("============================ POSTING altpartlist4 ============================")
##            print (altpartlist3)

            if(altpartlist4):
                altpartlistlink4=re.compile('src="(.+?)"').findall(altpartlist4[0])
##                print ("============================ POSTING altpartlistlink4 ============================")
##                print (altpartlistlink4)
                for vlink in altpartlistlink4:
                    name = name + ' (LQ)'
                    videomega(vlink,name)

               
        partctr=0
        if(len(partlist)>0):
               partlink=re.compile('sources(.+?)Part').findall(partlist[0])
##               print ("============================ POSTING partlink ============================")
##               print (partlink)

               #no parts
               if(len(partlink) == 1):
                   for vlink in partlink:
                       addDir(name.decode("utf-8"),vlink,3,"")

               elif(len(partlink) > 1):
                   playList = ''
                   for vlink in partlink:
                       partctr=partctr+1
                       addDir(name.decode("utf-8") + " Part " + str(partctr),vlink,3,"")
                       playList = playList + vlink +";#"

                   addDir('------------->[B]PLAY ALL[/B]<------------- [I]Watch all ' + str(partctr) + ' parts[/I]',playList,3,'')

        #eng subs
        if (len(engsubsNone)<1):
            partctr2=0
            if(len(partlist2)>0):
                   partlink2=re.compile('sources(.+?)Part').findall(partlist2[0])
##                   print ("============================ POSTING partlink2 ============================")
##                   print (partlink2)

                   #no parts (eng subs)
                   if(len(partlink2) == 1):
                       for vlink in partlink2:
                           addDir(name.decode("utf-8")  +  ' (English subs)',vlink,3,"")
                   
                   if(len(partlink2) > 1):
                       playList2 = ''
                       for vlink2 in partlink2:
                           partctr2=partctr2+1
                           addDir(name.decode("utf-8") + " Part " + str(partctr2) + " (English subs)",vlink2,3,"")
                           playList2 = playList2 + vlink2 +";#"

                       addDir('------------->[B]PLAY ALL[/B]<------------- [I]Watch all ' + str(partctr2) + ' parts[/I]' +  ' (English subs)',playList2,3,'')
       
        return partctr


def videomega(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        try:
                encodedurl=re.compile('unescape.+?"(.+?)"').findall(link)
        except:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok("wareztuga.tv",'This file is no longer available in VideoMega.')
                return
        encodedurl=re.compile('unescape.+?"(.+?)"').findall(link)
        teste=urllib.unquote(encodedurl[0])
##        print ("============================ POSTING teste ============================")
##        print (teste)
        
        mega=re.compile('file: "(.+?)"').findall(teste)
        for url in mega:
            try:
                addDir2('Watch ' + name,url,8,"")
            except:
                addDir2('Watch ' + name.decode("utf-8"),url,8,"")
##            xbmcPlayer = xbmc.Player()
##            xbmcPlayer.play(url)



def altParts(url,name):
##        print ("============================ POSTING alturl ============================")
##        print (url)
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        try:
            link=response.read()
            response.close()
        except: link = GetContent(url)

        link = ''.join(link.splitlines()).replace('\'','"').replace('\t','').replace('\\','')

        partlist=re.compile('function chsplayer(.+?)\}\)').findall(urllib.unquote(link).decode('utf-8'))
        partlist2=re.compile('function engplayer(.+?)\}\)').findall(urllib.unquote(link).decode('utf-8'))
        engsubsNone=re.compile('eng2222 \{[^>]*display: none').findall(urllib.unquote(link).decode('utf-8'))
               
        partctr=0
        if(len(partlist)>0):
               partlink=re.compile('sources(.+?)Part').findall(partlist[0])
##               print ("============================ POSTING partlink ============================")
##               print (partlink)

               #no parts
               if(len(partlink) == 1):
                   for vlink in partlink:
                       addDir(name.decode("utf-8"),vlink,3,"")

               elif(len(partlink) > 1):
                   playList = ''
                   for vlink in partlink:
                       partctr=partctr+1
                       addDir(name.decode("utf-8") + " Part " + str(partctr),vlink,3,"")
                       playList = playList + vlink +";#"

                   addDir('------------->[B]PLAY ALL[/B]<------------- [I]Watch all ' + str(partctr) + ' parts[/I]',playList,3,'')

        #eng subs
        if (len(engsubsNone)<1):
            partctr2=0
            if(len(partlist2)>0):
                   partlink2=re.compile('sources(.+?)Part').findall(partlist2[0])
##                   print ("============================ POSTING partlink2 ============================")
##                   print (partlink2)

                   #no parts (eng subs)
                   if(len(partlink2) == 1):
                       for vlink in partlink2:
                           addDir(name.decode("utf-8")  +  ' (English subs)',vlink,3,"")
                   
                   if(len(partlink2) > 1):
                       playList2 = ''
                       for vlink2 in partlink2:
                           partctr2=partctr2+1
                           addDir(name.decode("utf-8") + " Part " + str(partctr2) + " (English subs)",vlink2,3,"")
                           playList2 = playList2 + vlink2 +";#"

                       addDir('------------->[B]PLAY ALL[/B]<------------- [I]Watch all ' + str(partctr2) + ' parts[/I]' +  ' (English subs)',playList2,3,'')
       
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
        newlink = ''.join(link.splitlines()).replace('\t','').replace('http://tvbdo.com','http://www.tvbdo.com').replace('/show','http://www.tvbdo.com/show')
        
        #findEpisodeLink = re.compile('<h2><strong><a href="(.+?)">(.+?)</a>').findall(newlink)

	findEpisodeLink = re.compile('<span class="episode_loop"><a href="(.+?)">(.+?)</a>').findall(newlink)

##        print ("============================ POSTING newlink ============================")
##        print newlink

        if findEpisodeLink:
            for (vurl,tmp) in findEpisodeLink:
                try:
                    findEpisodes(url_fix(vurl),name,newmode)
                except:
                    findEpisodes(url_fix(vurl),name.decode("utf-8"),newmode)
        else:
            CheckParts(url,name)

    #except: pass


def findEpisodes(url,name,newmode):
    #try:
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
        
        newlink = ''.join(link.splitlines()).replace('\t','').replace('http://tvbdo.com','http://www.tvbdo.com').replace('/show','http://www.tvbdo.com/show')

        listcontent=re.compile('<div id="main">(.+?)</body>').findall(newlink)
	#print ("============================ POSTING listcontent ============================")
        #print listcontent

        if(newmode==5):
                vidmode=11
        else:
                vidmode=15

        #match=re.compile('<a class="clip-link" data-id="(.+?)" title="(.+?)" href="(.+?)">').findall(urllib.unquote(listcontent[0]).decode('utf-8'))

	match=re.compile('<span class="episode_loop">(.+?)<a href="(.+?)">(.+?)</a>').findall(urllib.unquote(listcontent[0]).decode('utf-8'))


	#print ("============================ POSTING match ============================")
        #print match
        
        for (vtmp,vurl,vname) in match:
            vname = vname.replace('&#8211;','-').replace('&#8217;','\'')
            try:
                addDir(name + ' - ' + vname,url_fix(vurl),vidmode,"")
            except:
                addDir(name + ' - ' + vname.decode("utf-8"),url_fix(vurl),vidmode,"")
	

        pagecontent=re.compile('<div class="loop-nav-inner">(.+?)</div>').findall(newlink)        
        if(len(pagecontent)>0):
                match5=re.compile('<a [^>]* href="(.+?)">(.+?)</a>').findall(pagecontent[0])
                for (vurl,vname) in match5:
                    vname = vname.replace('&laquo;','<<').replace('&raquo;','>>')
                    if(newmode==5):
                        try:
                            addDir('[COLOR yellow]page: [/COLOR]' + vname,vurl,17,'')
                        except:
                            addDir('[COLOR yellow]page: [/COLOR]' + vname.decode('utf-8'),vurl,17,'')
                    else:
                        try:
                            addDir('[COLOR yellow]page: [/COLOR]' + vname,vurl,18,'')
                        except:
                            addDir('[COLOR yellow]page: [/COLOR]' + vname.decode('utf-8'),vurl,18,'')          

    #except: pass


def Episodes2(url,name,newmode):
    #try:
##        try:
##            url = urllib.unquote(url.encode('utf-8'))
##        except: pass
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
        
        newlink = ''.join(link.splitlines()).replace('\t','')
      
        match = re.compile('<div class="entry-embed"><iframe src="(.+?)" [^>]*></iframe>').findall(newlink)

        for (vurl) in match:
            try:
                addDir('Watch ' + name,url_fix(vurl),15,"")
            except:
                addDir('Watch ' + name.decode("utf-8"),url_fix(vurl),15,"")

    #except: pass


def PlayUrlSource(url,name):
    try:

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
        #newlink = ''.join(link.splitlines()).replace('\t','').replace('href="/file','href="http://www.putlocker.com/file')
 

	newlink = ''.join(link.splitlines()).replace('\t','').replace('http://tvbdo.com','http://www.tvbdo.com').replace('streamvib.com','www.streamvib.com')

        listcontent=re.compile('<div id="main">(.+?)</body>').findall(newlink)
##	print ("============================ POSTING listcontent ============================")
##      print listcontent


        match=re.compile('jwplayer(.+?)file: "(.+?)"').findall(urllib.unquote(listcontent[0]).decode('utf-8'))        

##        print ("============================ POSTING match ============================")
##        print match

        for (vtmp,vurl) in match:
            try:            
                addDir2('Watch ' + name,vurl,20,"")
            except:
                addDir2('Watch ' + name.decode("utf-8"),vurl,20,"")


#       english subs
        match2=re.compile('Switch to:(.+?)English Sub').findall(urllib.unquote(listcontent[0]).decode('utf-8'))
        if match2:
            engURL = url + '?mirror=2'
            PlayUrlSource2(engURL,name)

##        for (vtmp,vurl) in match:
##            xbmcPlayer = xbmc.Player()
##            xbmcPlayer.play(vurl)
        
    except:
        d = xbmcgui.Dialog()
        d.ok(url,"Sorry, the content has been removed.","Please visit site to verify.")
            

def PlayUrlSource2(url,name):
    try:

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

	newlink = ''.join(link.splitlines()).replace('\t','').replace('http://tvbdo.com','http://www.tvbdo.com').replace('streamvib.com','www.streamvib.com')

        listcontent=re.compile('<div id="main">(.+?)</body>').findall(newlink)

        match=re.compile('jwplayer(.+?)file: "(.+?)"').findall(urllib.unquote(listcontent[0]).decode('utf-8'))

        for (vtmp,vurl) in match:
            try:
                addDir2('Watch ' + name + ' (English subs)',vurl,20,"")
            except:
                addDir2('Watch ' + name.decode("utf-8") + ' (English subs)',vurl,20,"")

##        for (vtmp,vurl) in match:
##            xbmcPlayer = xbmc.Player()
##            xbmcPlayer.play(vurl)
        
    except:
        d = xbmcgui.Dialog()
        d.ok(url,"Sorry, the content has been removed.","Please visit site to verify.")



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
##        try:
##            url = urllib.unquote(url.encode('utf-8'))
##        except: pass
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
    #try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    #except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

##def playVideo(videoType,videoId):
##    url = ""
##    #print videoType + '=' + videoId
##    if (videoType == "youtube"):
##        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
##        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
##    elif (videoType == "vimeo"):
##        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
##    elif (videoType == "tudou"):
##        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
##    else:
##        xbmcPlayer = xbmc.Player()
##        xbmcPlayer.play(videoId)


def playVideo(url,name):
    GA("playVideo",name)
    xbmc.executebuiltin("XBMC.Notification(Please Wait!, Loading video link into XBMC Media Player,5000)")
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)

def loadVideos(url,name):
    try:
       GA("LoadVideo",name)

       links=url.split(';#')

##       print ("============================ POSTING links ============================")
##       print links

       framecontent = url
##       print ("============================ POSTING framecontent ============================")
##       print framecontent

##       vlinkplayList=''
##       vlinkplayList2=''

       qualOrder1 = re.compile('":\[\{"label":"720p"(.+?)file').findall(framecontent)
       qualOrder2 = re.compile('":\[\{"label":"480p"(.+?)file').findall(framecontent)
       qualOrder3 = re.compile('":\[\{"label":"360p"(.+?)file').findall(framecontent)
       
       if qualOrder1:
           qualityval = ["720p(MP4)","480p(FLV))","360p(FLV)","360p(MP4)","240p(FLV)"]
       elif qualOrder2:
           qualityval = ["480p(FLV))","360p(FLV)","360p(MP4)","240p(FLV)"]
       elif qualOrder3:
           qualityval = ["360p(FLV)","360p(MP4)","240p(FLV)"]
       else:
           qualityval = ["240p(FLV)","360p(MP4)","360p(FLV)","480p(FLV)","720p(MP4)"]

##       vlink = re.compile('\'(.+?)\'').findall(embedlink[0])
##       print ("============================ POSTING vlink ============================")
##       print vlink
##
##       for vvlink in vlink:
##           print ("============================ POSTING vvlink ============================")
##           print vvlink
##           vlinkplayList = vlinkplayList + vvlink +";#"
##           print ("============================ POSTING vlinkplayList ============================")
##           print vlinkplayList
##
##           if match2:
##               framecontent2 = json.dumps(match2).replace('\\','').replace('""','",\;"')
##               embedlink2 = re.compile('\;(.+?)\;').findall(urllib.unquote(framecontent2).decode('utf-8'))
##               vlink2 = re.compile('"file":"(.+?)"\,').findall(embedlink2[0])
##               for vvlink2 in vlink2:
##                   vlinkplayList2 = vlinkplayList2 + vvlink2 +";#"

       embedlink = re.compile('"file":"(.+?)"').findall(framecontent)
##       print ("============================ POSTING embedlink ============================")
##       print embedlink

       qctr=0
       print ("============================ POSTING length links ============================")
       print len(links)
       if(len(links) < 2):
           for vname in embedlink:
##               print ("============================ POSTING vname ============================")
##               print vname
               #if(len(embedlink) > 0):
               addLink(qualityval[qctr],urllib.unquote(embedlink[qctr]),8,"","")
               qctr=qctr+1
                                                  
       elif(len(links) > 1):
           newrange = len(links) - 1
##           print ("============================ POSTING newrange ============================")
##           print newrange

           framecontent2 = url.split(';#')
##           print ("============================ POSTING framecontent2 ============================")
##           print framecontent2

           a=0
           b=1
           c=2
           d=3
           e=4
           parts123Links0 = ''
           parts123Links1 = ''
           parts123Links2 = ''
           parts123Links3 = ''
           parts123Links4 = ''
           
           for i in range(newrange):
               allPartlinks = re.compile('"file":"(.+?)"').findall(framecontent2[i])
               linkslength = len(allPartlinks)    

           for k in range(newrange):
               parts123Links0 =  parts123Links0 + embedlink[a] + ";#"
               a=a+linkslength
               if linkslength > 1:
                   parts123Links1 =  parts123Links1 + embedlink[b] + ";#"
                   b=b+linkslength
               if linkslength > 2:
                   parts123Links2 =  parts123Links2 + embedlink[c] + ";#"
                   c=c+linkslength                   
               if linkslength > 3:
                   parts123Links3 =  parts123Links3 + embedlink[d] + ";#"
                   d=d+linkslength
               if linkslength > 4:
                   parts123Links4 =  parts123Links4 + embedlink[e] + ";#"
                   e=e+linkslength

           addLink(qualityval[0],parts123Links0,16,"","")
           if len(allPartlinks) > 1:
               addLink(qualityval[1],parts123Links1,16,"","")
           if len(allPartlinks) > 2:
               addLink(qualityval[2],parts123Links2,16,"","")
           if len(allPartlinks) > 3:
               addLink(qualityval[3],parts123Links3,16,"","")
           if len(allPartlinks) > 4:
               addLink(qualityval[4],parts123Links4,16,"","")               
           
       else:
           #match=re.compile('<script type="text\/javascript">(.+?)var language').findall(urllib.unquote(newlink))
           if(len(match) > 0):
               loadVideos(match[0],name)
           else:
               d = xbmcgui.Dialog()
               d.ok('Not Implemented','Sorry this video site is ',' not implemented yet')
          
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Sorry, the content has been removed.","Please visit site to verify.")
       
def PLAYLIST_VIDEOLINKS(name,url):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)        
        links=url.split(';#')
        print "linksurl" + str(url)
##        print "-------------posting links-------------"
##        print links
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = -1
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                #loadPlaylist(videoLink,name)
                print "-------------posting videoLink-------------"
                print videoLink
                print "-------------posting links-------------"
                print links
		CreateList("other",urllib2.unquote(videoLink).decode("utf8"))
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
                d.ok('videourl: ' + str(playList), 'One or more of the playlist items may be removed.','Please check links individually.')
        return ok


def CreateList(videoType,videoLink):
    url1 = ""
    if (videoType == "youtube"):
        url1 = getYoutube(videoLink)
    elif (videoType == "vimeo"):
        url1 = getVimeoVideourl(videoId)
    elif (videoType == "tudou"):
        url1 = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
        url1=videoLink

    if(len(videoLink) >0):
        print "posting url1"
        print url1
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=url1, listitem=liz)


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
##    ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
        print "============================ POSTING UA response ============================"
##        print (response)
##        print "============================ POSTING UA utm_url ============================"
##        print (utm_url)  
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

def addDir2(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
elif mode==17:
       findEpisodes(url,name,5)
elif mode==18:
       findEpisodes(url,name,mode)
elif mode==19:
       findEpisodes2(url,name,mode)
elif mode==20:
        playVideo(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
