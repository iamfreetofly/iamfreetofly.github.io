### ############################################################################################################
###	#	
### # Site: 				#		iLiVE - http://www.ilive.to/
### # Author: 			#		The Highway
### # Description: 	#		
### # Credits: 			#		Originally ported from the addon project known as Mash Up - by Mash2k3 2012.
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import xbmc,xbmcgui,xbmcaddon,xbmcplugin,urllib,urllib2,re,cookielib,os,sys,time,math,datetime
print sys.argv
#from resources.libs import main
from common import *
from common import (_addon,addon,_plugin,net,_artIcon,_artFanart,PlayItCustom,_addonPath,_SaveFile,_OpenFile,_datapath,_debugging)
selfAddon=_plugin
#from universal import watchhistory
#wh=watchhistory.WatchHistory(ps('_addon_id'))
### ############################################################################################################
### ############################################################################################################
SiteName='[COLOR lime]i[COLOR white]LiVE[/COLOR][/COLOR]  [v0.2.4]  [Streams] * (2015-01-03)'
SiteTag='ilive.to'
mainSite='http://www.ilive.to/'
iconSite='http://www.ilive.to/images/logo.png' #_artIcon #http://website.informer.com/thumbnails/280x202/i/ilive.to.png
#	#https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash1/373452_141569702620837_539306243_n.jpg
#	#http://www.ilive.to/images/logo.png
#	#http://www.google.com/url?sa=i&source=images&cd=&cad=rja&docid=bjuYU3p5ns4T3M&tbnid=QscctgKwdsQrBM:&ved=0CAUQjBwwAA&url=http%3A%2F%2Fwww.lifepr.de%2Fattachment%2F262095%2FiLive_Digital_Logo_on_black.jpg&ei=wolHUoaZLdTUyQHUvIF4&psig=AFQjCNHHEGJ8lHifkX1TFQyRd7Vgqd8qKg&ust=1380506434767500
#	#http://www.pwrnewmedia.com/2009/ilive91218/assets/iLive_Logo2FINAL.jpg
#	#http://www.alliance-mktg.com/assets/1/12/GalleryMainDimensionId/iLive_Site_Logo.JPG
#	#http://www.brandsoftheworld.com/sites/default/files/styles/logo-thumbnail/public/112011/logoilive.ai_.png
#	#http://media.marketwire.com/attachments/200712/387150_logo.jpg
#	#https://si0.twimg.com/profile_images/1376125989/logo-1.jpg
#	#
#	#
fanartSite='http://www.iliveconference.com/wp-content/gallery/home-slider/thumbs/thumbs_ilive.png' #_artFanart
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
### ############################################################################################################
site=addpr('site','')
section=addpr('section','')
url=addpr('url','')
sections={'series':'series','movies':'movies'}
thumbnail=addpr('img','')
fanart=addpr('fanart','')
page=addpr('page','')
### ############################################################################################################
### ############################################################################################################
ApiLiveDomain=addst('DefaultApiLiveList','Default'); 
if   ApiLiveDomain=='ilive.to': doMain="http://www.ilive.to/"; 
elif ApiLiveDomain=='streamlive.to': doMain="http://www.streamlive.to/"; 
else: doMain="http://www.streamlive.to/"; 
headers={'Referer':doMain}; 
try: UrlTAG=addst('url-tag')
except: UrlTAG='view'


### ############################################################################################################
### ############################################################################################################
CookieJar=xbmc.translatePath(os.path.join(_datapath,'cookies.txt'))
UseAccount=tfalse(addst('enable-accountinfo','false')); 
AccountUsername=addst('username',''); 
AccountPassword=addst('password',''); 
if len(AccountUsername)==0: UseAccount=False
elif len(AccountPassword)==0: UseAccount=False

### ############################################################################################################
### ############################################################################################################
def About(head=''+cFL(SiteName,'blueviolet')+'',m=''):
	m=''
	if len(m)==0:
		m+='IRC Chat:  '+cFL('#XBMCHUB','blueviolet')+' @ '+cFL('irc.Freenode.net','blueviolet')
		m+=CR+'Site Name:  '+SiteName+CR+'Site Tag:  '+SiteTag+CR+'Site Domain:  '+mainSite+CR+'Site Icon:  '+iconSite+CR+'Site Fanart:  '+fanartSite
		m+=CR+'Age:  Please make sure you are of a valid age to watch the material shown.'
		m+=CR+CR+'Known Hosts for Videos:  '
		m+=CR+'RTMP Live Streams'
		m+=CR+CR+'Features:  '
		m+=CR+'* Includes my Increased List of Categories.  '
		m+='Those which often have no items are marked as such.  '
		m+='Some of My English Shortcuts are included as well.'
		m+=CR+'* Browse Live Channels.'
		m+=CR+'* Play Live Channels.'
		m+=CR+CR+'Notes:  '
		m+=CR+'* Originally ported from mash2k3\'s Mash UP.'
		m+=CR+'* This Project has been given a major overhaul and been reworked to work with my own project\'s functions and methods.'
		#m+=CR+'* Checkout:  Try the iLiVE, CAST ALBA TV, and the rest of Mash Up @ Mash2k3\'s Repo.'
		m+=CR+'* If you really enjoy these addons, please check out the originals'
		m+=CR+'* Some -ORIGINALS- may or may not have stuff like GA-Tracking, Advertisements....'
		m+=CR+'* Some Sub-Addons may be outdated.  Please check their repos for the latest version of their Full-Fledge Addon(s).'
		m+=CR+CR+'Changes:  '
		#m+=CR+'* '
		#m+=CR+'* '
		#m+=CR+'** '
		#m+=CR+'** '
		m+=CR+'* v0.0.9'
		m+=CR+'** Fix for playable link.'
		m+=CR+'* v0.0.8'
		m+=CR+'** '
		m+=CR+'* v0.0.7'
		m+=CR+'** FlashPlayer captcha fixed.'
		m+=CR+'* v0.0.6'
		m+=CR+'** Fixing Streams not listed.'
		m+=CR+'** Fixed Number of Pages.'
		m+=CR+'** Added Movies Category.'
		m+=CR+'* v0.0.5'
		m+=CR+'** Re-did Token Method.  Thanks to BlazeTamer.'
		m+=CR+'* v0.0.4'
		m+=CR+'** Re-did Browsing menus.'
		m+=CR+'** Added Language and Sort setting menus.'
		m+=CR+'** Re-did Pagination Method.'
		m+=CR+"** Added BlazeTamer's method to fix token."
		#m+=CR+'* '
		m+=CR+''
		m+=CR+ps('ReferalMsg')
		m+=CR+''
		m+=CR+''
		m+=CR+''
	String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	#RefreshList()

### ############################################################################################################
### ############################################################################################################
def DoE(e): xbmc.executebuiltin(E)
def DoA(a): xbmc.executebuiltin("Action(%s)" % a)
# DoA("Back"); 

try: from sqlite3 import dbapi2 as orm
except: from pysqlite2 import dbapi2 as orm
DB='sqlite'; DB_DIR=os.path.join(xbmc.translatePath("special://database"),'Textures13.db'); 
if os.path.isfile(DB_DIR)==True: print "Texture Database Found: "+DB_DIR; 
else: print "Unable to locate Texture Database"

def unCacheAnImage(url):
	if os.path.isfile(DB_DIR)==True: 
		db=orm.connect(DB_DIR); 
		#g='Select cachedurl FROM texture WHERE url = "'+url+'";'; print g; 
		#a=db.execute(g); print str(a); 
		s='DELETE FROM texture WHERE url = "'+url+'";'; #print s; 
		db.execute(s); 
		db.commit(); db.close(); 

### ############################################################################################################
### ############################################################################################################

def getToken(url):
	#return 'I8772LDKksadhGHGagf'
	html=net.http_GET(url).content
	token_url=re.compile('\$.getJSON\("(.+?)",').findall(html)[0]
	#import datetime,time
	time_now=datetime.datetime.now()
	epoch=time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
	epoch_str=str('%f' % epoch); epoch_str=epoch_str.replace('.',''); epoch_str=epoch_str[:-3]
	token_url=token_url + '&_=' + epoch_str
	#
	tokhtml=net.http_GET(token_url+'&_='+str(epoch), headers={'Referer':url}).content
	debob('tokhtml: ')
	debob(tokhtml)
	token=re.compile('":"(.+?)"').findall(tokhtml)[0]
	token=re.compile('":"(.+?)"').findall(net.http_GET(token_url+'&_='+str(epoch), headers={'Referer':url}).content)[0]
	#if '#' in token: token=token.split('#')[0]
	#if '#' in token: token=token.split('#')[1]
	#if '#' in token: token=token.split('#')[0]+token.split('#')[1]
	debob(token)
	return token
def doCtoD(c):
	if len(c) > 0:
		d=""; ic=len(c); i=0; 
		while (i<ic):
			try:
				if i%3==0: d+="%";
				else: d+=c[i]
			except: pass; debob({'d[error]':d})
			i=i+1
		debob({'d':d})
		d=urllib.unquote_plus(d)
		debob({'du':d})
		return d
	else: return ''
def doXTtoXZ(x,tS,b=1024,p=0,s=0,w=0,r2=''):
		l=len(x); t=tS.split(','); r=[]
		
		for j in range(int(math.ceil(l/b)),0, -1):
			for i in range(min(l,b),0, -1):
				w |= int(t[ord(x[p])-48]) << s
				p += 1
				if (s):
					r.append(chr(165 ^ w & 255))
					w >>= 8
					s -= 2
				else:
					s = 6
			l -=1
		r = ''.join(r)
		return r
		
		#j=math.ceil(l/b);
		#while j>0:
		#	r='';
		#	#i=math.min(l,b);
		#	i=min(l,b);
		#	while i>0:
		#		try:
		#			p=p+1
		#			#print ord(x[p])
		#			#print int(t[int(x[p])])
		#			#print (int(t[int(x[p])])-48])
		#			w|=((int(t[ord(x[p])-48])))<<s;
		#			###w|=(int(t[x[p++]-48]))<<s;
		#			if s:
		#				#r+=''.join(map(unichr, 165^w&255))
		#				#r+=chr(165^w&255)
		#				r+=unichr(165^w&255)
		#				#r+=string.fromCharCode(165^w&255);
		#				w>>=8;
		#				s-=2
		#			else: s=6
		#		except: pass; #print r
		#	r2+='\n\r'+r; #document.write(r)
		#	print r
		#	i=i-1; l=l-1
		#	j=j-1
		#return r2
def iLivePlay(mname='',murl='',thumb='',LinkNo=''):
	#if '.to/view/' in murl: murl=murl.replace('.to/view/','.to/view-channel/')
	#if '.to/view/' in murl: murl=murl.replace('.to/view/','.to/watch-channel/')
	if '.to/view/' in murl: murl=murl.replace('.to/view/','.to/%s/'%UrlTAG)
	
	menuurl=""+murl; name=mname; #ApiLiveDomain=addst('DefaultApiLiveList','Default')
	# #artwork='http://addonrepo.com/xbmchub/moviedb/images/'
	# ###
	#linkA=nURL('http://www.ilive.to/server.php?',headers={'Referer': 'http://www.ilive.to/'}); 
	#match=re.compile('{"token":"(.+?)"}').findall(linkA); 
	#for token in match:
	debob({'menuurl':menuurl,'LinkNo':LinkNo,'mname':mname}); 
	if (str(LinkNo)=='99') and (UseAccount==True):
		DayLoggedIn=addst('dayloggedin','')
		DayLoggedInNew=str(datetime.date.today().day)
		if (isFile(CookieJar)==False) or (DayLoggedIn != DayLoggedInNew):
			if '://ilive.to/' in menuurl: loginurl='http://ilive.to/login.php'
			elif '://streamlive.to/' in menuurl: loginurl='http://streamlive.to/login.php'
			else: loginurl='http://streamlive.to/login.php'
			GetLogin=nURL(loginurl,method='post',headers={'Referer':menuurl},form_data={'username':AccountUsername,'password':AccountPassword,'submit':'Login'},cookie_file=CookieJar,save_cookie=True)
			addstv('dayloggedin',DayLoggedInNew)
		link=nURL(menuurl,cookie_file=CookieJar,load_cookie=True)
	else:
		link=nURL(menuurl) #OPEN_URL(menuurl)
	
	deb('Length of html',str(len(link))); 
	#_SaveFile(os.path.join(_addonPath,'link1.html'),link); deb('saved','link1.html')
	try: _SaveFile(os.path.join(_addonPath,'link1.html'),link); deb('saved','link1.html')
	except: pass
	
	#deb(str(len(link)),os.path.join(_addonPath,'link.html')); 
	## ### ## 
	##vID=re.compile('(?:view|view-channel|watch-channel)?/(\d+)').findall(menuurl)[0]
	#vID=re.compile('\D+-channel/(\d+)').findall(menuurl)[0]
	vID=re.compile(UrlTAG+'/(\d+)').findall(menuurl)[0]
	
	menuurl2='http://www.mobileonline.tv/channel.php?n=%s'%vID
	TimeOut=str(addst('DefaultTimeOut','15'))
	SleeperTime=str(addst('DefaultSleepBeforePlay','4000'))
	
	#LinkNo='99'
	if not str(LinkNo)=='99':
		link2=nURL(menuurl2)
		## ### ## 
		if LinkNo=='': LinkNo=addst('DefaultVideoLink','2')
		if LinkNo=='': LinkNo=2
		if LinkNo=='0HLS':  LinkNo=0
		if LinkNo=='1RTMP': LinkNo=1
		if LinkNo=='2RTSP': LinkNo=2
		else: LinkNo=int(LinkNo)
		## ### ## 
		debob({'LinkNo':LinkNo})
		#playable=re.compile('<p style="font-size:30px;"><a href=(\D+://.+?) target="_blank">Link').findall(link2)[int(LinkNo)] #0-2, 0:http, 1:rtmp, 2:rtsp
		playables=re.compile('<p style="font-size:30px;"><a href=(\D+://.+?) target="_blank">Link').findall(link2)
		debob({'playables':playables}); 
		playable=playables[int(LinkNo)] #0-2, 0:http, 1:rtmp, 2:rtsp
		## ### ## 
		if not TimeOut=='0': playable+=' app=%s live=1 timeout=%s'%('',TimeOut)
		try: xbmc.sleep(int(SleeperTime))
		except: pass
		PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)
		return
		## ### ## 
	## ### ## 
	if '<script language=javascript>c="' in link:
		deb('method','encrypted')
		#debob({'link':link}); 
		c=re.compile('<script language=javascript>c="(.+?)"').findall(link)[0]; #debob({'c':c}); 
		cu=urllib.unquote_plus(c); #debob({'cu':cu}); 
		d=doCtoD(c); #debob({'d':d}); 
	#	#if len(c) > 0:
	#	#	d=""; ic=len(c); i=0; d2=[]; 
	#	#	while (i<ic):
	#	#	#	try: d+='%'+c[i]+c[i+1]
	#	#	#	except: debob({'d[error]':d})
	#	#	#	debob({'d':d})
	#	#		try:
	#	#	#		if c[i]=='@':
	#	#			if i%3==0:
	#	#				d+="%";
	#	#			else:
	#	#				d+=c[i]
	#	#	#			d2+=c[i]
	#	#	#			debob({'d2':d2})
	#	#	#			debob({'d2u':urllib.unquote_plus(d2)})
	#	#	#			d2=''
	#	#	#		else:
	#	#	#			d2+='%'+c[i]+c[i+1]
	#	#		except: debob({'d[error]':d,'d2[error]':d2})
	#	#		i=i+1
	#	#debob({'d':d,'d2':d2})
	#	#du=urllib.unquote_plus(d); debob({'du':du}); 
	#	
	#	#e=re.compile('";\s*eval(unescape("(.+?)"').findall(link)[0]; debob({'e':e}); 
	#	#eu=urllib.unquote_plus(e); debob({'eu':eu}); 
	#	
		t=re.compile('t=Array\(([0-9,]+)\)').findall(d)[0]; #debob({'t':t}); 
		x=re.compile('"\)\);\s*x\("(.+?)"').findall(link)[0]; #debob({'x':x}); 
		z=doXTtoXZ(x,t); #debob({'z':z}); 
		
		
		#html=''+z; 
		link=''+z; 
		#debob(link)
		#return
		## ### ## 
	## ### ## 
	else:
		deb('method','encryption not found')
	## ### ## 
	ok=True
	grabNo=0 #-1
	
	##link=nURL(menuurl) #OPEN_URL(menuurl)
	
	if link:
			deb(str(len(link)),os.path.join(_addonPath,'link.html')); 
			#_SaveFile(os.path.join(_addonPath,'link.html'),link.decode('utf-8'))
			#try: 
			_SaveFile(os.path.join(_addonPath,'link.html'),link); deb('saved','link.html')
			#except: pass
			
			#if '<span class="viewers">0</span>' in link: 
			#	debob({'mname':mname,'murl':murl,'error':'Channel Offline or no viewers'}); 
			#	popOK(msg="This Channel has ",title="Channel Status.",line2="no vewiers at the moment ",line3="and may be offline."); 
			#	eod(); return
			if ('<span class="viewers">0</span>' in link) and ('<span class="totalviews">0</span>' in link): 
				debob({'mname':mname,'murl':murl,'error':'Channel Offline'}); 
				popOK(msg="This Channel is ",title="Channel Unavailable.",line2="offline at the moment.",line3=""); 
				eod(); return
			#elif UseAccount==True: pass
			elif '<h3 class="na_msg">This channel is domain protected.<br/>Please upgrade your account to Premium to watch.<br/>Click here to <a href="http://www.streamlive.to/premium">upgrade to Premium account</a>.</h3>' in link: 
				debob({'mname':mname,'murl':murl,'error':'Premium Channel'}); 
				if UseAccount==True:
					popOK(msg="This Channel is ",title="Channel might be unavailable.",line2="a Premium Channel.",line3=""); 
				else: 
					popOK(msg="This Channel is ",title="Channel Unavailable.",line2="a Premium Channel.",line3=""); 
					eod(); return
			elif '<h3 class="na_msg">This channel is domain protected.<br/>Please upgrade your account to Premium to watch.<br/>Click here to <a href="http://www.ilive.to/premium">upgrade to Premium account</a>.</h3>' in link: 
				debob({'mname':mname,'murl':murl,'error':'Premium Channel'}); 
				if UseAccount==True:
					popOK(msg="This Channel is ",title="Channel might be unavailable.",line2="a Premium Channel.",line3=""); 
				else: 
					popOK(msg="This Channel is ",title="Channel Unavailable.",line2="a Premium Channel.",line3=""); 
					eod(); return
			
			
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
			#matchserv=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)
			#for server in matchserv:
			#	print 'Server IS '+server; headers={'Referer':'http://www.ilive.to/'}; url=server; html=net.http_GET(url,headers=headers).content; match=re.compile('{"token":"(.+?)"}').findall(html)
			#	for token in match: print 'SERVERTOKEN IS  '+token; token=token
			#try: 
			server=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)[0]
			#except:
			#	debob({'mname':mname,'murl':murl,'error':'Channel Offline or unable to find server'}); 
			#	popOK(msg="This Channel is ",title="Channel Unavailable.",line2="offline at the moment.",line3="Unable to find Server."); 
			#	eod(); return
			print 'Server IS '+server; url=server; 
			
			#headers={'Referer':'http://www.ilive.to/'}; 
			#if   ApiLiveDomain=='ilive.to': headers={'Referer':'http://www.ilive.to/'}; 
			#elif ApiLiveDomain=='streamlive.to': headers={'Referer':'http://www.streamlive.to/'}; 
			#else: headers={'Referer':'http://www.streamlive.to/'}; 
			
			##html=net.http_GET(url,headers=headers).content; 
			html=nURL(url,headers=headers)
			token=re.compile('{"token":"(.+?)"}').findall(html)[0]
			debob({'token':token,'lengthofhtml':len(html),'server':server}); 
			###
			#match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
			#vid=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)[0]
			#vid=re.compile('http://www.ilive.to/embed/(\d+)&width=\d*&height=\d*&autoplay=true').findall(link)[0]
			vid=re.compile('http://www.(?:streamlive.to|ilive.to)?/embed/(\d+)&width=\d*&height=\d*&autoplay=true').findall(link)[0]
			###
			#pageUrl='http://www.ilive.to'
			pageUrl=''+doMain
			#pageUrl='http://www.ilive.to/m/channel.php?n='+vid
			#pageUrl='http://www.ilive.to/view/%s/'%vid
			playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
			debob(playpath)
			#playpath=playpath[0]
			playpath=playpath[grabNo]
			newplaypath=str(playpath)        
			rtmp=re.compile('streamer: "(.+?)"').findall(link)
			debob(rtmp)
			#rtmp=rtmp[0]
			rtmp=rtmp[grabNo]
			newrtmp=str(rtmp)
			newrtmp=newrtmp.replace('\/','/').replace('\\','')
			app=''+newrtmp
			app=app.split('?xs=')[1]
			app2=re.compile('rtmp://[\.\w:]*/([^\s]+)').findall(newrtmp)[0]
			#try:		app=newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			#except:	app=newrtmp.replace('rtmp://watch1.ilive.to:1935/','')
			#try:		app=newrtmp.replace('rtmp://watch2.ilive.to:1935/','')
			#except:	app=newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			try:		ReplacementA=re.compile('(rtmp://[0-9A-Za-z]+\.(?:ilive\.to|streamlive\.to)?:\d+/)').findall(app)[0]
			except:	ReplacementA=''
			if len(ReplacementA) > 0: app=app.replace(ReplacementA,''); deb('removing',ReplacementA); 
			newapp=str(app)
			#link=nURL(pageUrl)
			try: swf=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)[0]
			except: swf=''
			if len(swf)==0: swf=doMain+'player/player_ilive_2.swf'
			#if len(swf)==0: swf='http://www.ilive.to/player/player_ilive_2.swf'
			
			###swf=re.compile('flashplayer: "(.+?)"').findall(link)[0]
			####swf=re.compile('flashplayer:\s+"(.+?\.swf)"').findall(link)[grabNo]
			####swf=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)[-1]
			####swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
			####for swf in swff: swf=swf; print 'SWF IS '+swf
			####playable =rtmp[0]+' app=edge/?xs='+app[1]+' playpath=' + newplaypath + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			####playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl='+swf+' live=1 timeout=15 token='+token+' swfVfy=1 pageUrl=http://www.ilive.to'
			###playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl='+swf+' live=1 timeout=15 token='+token+' swfVfy=1 pageUrl='+pageUrl
			###playable='%s app=%s playpath=%s swfUrl=%s live=1 timeout=%s token=%s swfVfy=1 pageUrl=%s' % (newrtmp,newapp,newplaypath,swf,'15',token,pageUrl)
			###playable='%s app=edge/?xs=%s playpath=%s swfUrl=%s live=true timeout=%s token=%s swfVfy=1 pageUrl=%s' % (newrtmp,newapp,newplaypath,swf,'15',token,pageUrl)
			##playable='%s app=edge/?xs=%s playpath=%s swfUrl=%s pageUrl=%s live=true timeout=%s token=%s' % (newrtmp,newapp,newplaypath,swf,pageUrl,'15',token)
			
			#playable='%s app=edge/?xs=%s playpath=%s swfUrl=%s pageUrl=%s live=%s timeout=%s token=%s app=%s'%(newrtmp,newapp,newplaypath,swf,pageUrl,'true','15',token,app2)
			playable='%s app=edge/?xs=%s playpath=%s swfUrl=%s pageUrl=%s live=%s timeout=%s token=%s'%(newrtmp,newapp,newplaypath,swf,pageUrl,'true',TimeOut,token)
			
			#
			print 'RTMP IS '+playable
			#LIVERESOLVE(name,playable,thumb)
			
			#try: 
			#PlayItCustomMT(url=murl,stream_url=playable,img=thumb,title=name)
			#except: 
			
			try: xbmc.sleep(int(SleeperTime))
			except: pass
			
			PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)
			
			###
			#for vid in match:
			#	pageUrl='http://www.ilive.to/m/channel.php?n='+vid
			#	playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
			#	playpath=playpath[0]
			#	newplaypath=str(playpath)        
			#	rtmp=re.compile('streamer: "(.+?)"').findall(link)
			#	rtmp=rtmp[0]
			#	newrtmp = str(rtmp)
			#	newrtmp = newrtmp.replace('\/','/').replace('\\','')
			#	#try:		app = newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			#	#except:	app = newrtmp.replace('rtmp://watch1.ilive.to:1935/','')
			#	#try:		app = newrtmp.replace('rtmp://watch2.ilive.to:1935/','')
			#	#except:	app = newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			#	#newapp = str(app)
			#	#link=OPEN_URL(pageUrl)
			#	#swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
			#	#for swf in swff:
			#	#	swf= swf
			#	#	#swf= swf[0]
			#	#	#Manual SWF Added
			#	#	#swf = 'http://www.ilive.to/player/player.swf'
			#	#	print 'SWF IS ' + swf
			#	#playable =newrtmp + ' app=' + newapp + ' playpath=' + newplaypath + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			#	##
			#	#print 'RTMP IS ' +  playable
			#	#LIVERESOLVE(name,playable,thumb)
			#
			#
			#match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
			#for fid in match:
			#	vid=fid; 
			#	pageUrl='http://www.ilive.to/m/channel.php?n='+fid; 
			#	server=re.compile('''.*getJSON\("([^'"]+)"''').findall(link); 
			#	playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)[0]; newplaypath=str(playpath); 
			#	swf=re.compile('flashplayer: "http://.+?.ilive.to/(.+?)"').findall(link)[0]; 
			#	rtmp=re.compile('streamer: "(.+?)"').findall(link)[0]; newrtmp=str(rtmp); newrtmp=newrtmp.replace('\/','/').replace('\\',''); 
			#	try: app=newrtmp.replace('rtmp://watch.ilive.to:1935/',''); 
			#	except: app=newrtmp.replace('rtmp://watch1.ilive.to:1935/',''); 
			#	try: app=newrtmp.replace('rtmp://watch2.ilive.to:1935/',''); 
			#	except: app=newrtmp.replace('rtmp://watch.ilive.to:1935/',''); 
			#	newapp=str(app); 
			#	#playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl='+newswf+' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			#	playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl=http://www.ilive.to/'+swf+' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			#	print 'RTMP IS ' +  playable
			#	#LIVERESOLVE(name,playable,thumb)
			#	PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)

def DoSearchLIVE(title=''):
	if len(title)==0: title=showkeyboard(txtMessage=title,txtHeader="Search:  ")
	if (title=='') or (title=='none') or (title==None) or (title==False): return
	deb('Searching for',title); #title=title.replace('+','%2B').replace('&','%26').replace('?','%3F').replace(':','%3A').replace(',','%2C').replace('/','%2F').replace('=','%3D').replace('@','%40').replace(' ','%20'); 
	deb('Searching for',title); 
	##
	iLiveBrowseLIVE(search=title); 
	##
def DoSearch(title=''):
	if len(title)==0: title=showkeyboard(txtMessage=title,txtHeader="Search:  ")
	if (title=='') or (title=='none') or (title==None) or (title==False): return
	deb('Searching for',title); title=title.replace('+','%2B').replace('&','%26').replace('?','%3F').replace(':','%3A').replace(',','%2C').replace('/','%2F').replace('=','%3D').replace('@','%40').replace(' ','%20'); 
	deb('Searching for',title); 
	##
	iLiveBrowse(search=title); 
	##
def iLiveBrowse(channel='',iLive_Sort='',iLive_Language='',search=''):
	if len(iLive_Sort)==0: iLive_Sort="0"
	#channel=channel.replace(" ","%20"); 
	### \/ Catching the first page.
	ApiLiveDomain=addst('DefaultApiLiveList','Default'); 
	if   ApiLiveDomain=='ilive.to': doMain="http://www.ilive.to/"; 
	elif ApiLiveDomain=='streamlive.to': doMain="http://www.streamlive.to/"; 
	else: doMain="http://www.streamlive.to/"; 
	headers={'Referer':doMain}; 
	if len(search) > 0: tUrl="%schannels/?q=%s"%(doMain,search)
	else: tUrl=doMain+"channels/"+channel.replace(" ","%20")+"?sort="+iLive_Sort+"&lang="+iLive_Language; 
	
	deb("url",tUrl); 
	html=nURL(tUrl,headers=headers); deb("length of first page",str(len(html))); 
	### \/ Catching the rest of the pages.
	if '<p align="center" class="pages"><strong>Page: </strong>' in html:
		phtml=html.split('<p align="center" class="pages"><strong>Page: </strong>')[1].split('</span></p>')[0]; deb("length of phtml",str(len(phtml))); 
		try: ppages=re.compile('<a href="(http://www.(?:ilive.to|streamlive.to)?/channels/.+?)">\s*(\d+)\s*</a').findall(phtml.replace('</a>','</a\n\r>'))
		except: ppages=[]
		deb("number of pages",str(len(ppages)+1)); debob(ppages); 
		dialogWait=xbmcgui.DialogProgress(); loaded=1; ptotal=len(ppages)+1; ret=dialogWait.create('Please wait...'); 
		percent=(loaded * 100)/ptotal; remaining_display='[B]Page '+str(loaded)+' of '+str(ptotal)+'[/B].'; dialogWait.update(percent,'[B]Loading Pages...[/B]',remaining_display); 
		for (ppage,pname) in ppages: 
			time.sleep(1); html+=nURL(ppage.replace(" ","%20")); 
			loaded=loaded+1; percent=(loaded * 100)/ptotal; remaining_display='[B]Page '+str(loaded)+' of '+str(ptotal)+'[/B].'; dialogWait.update(percent,'[B]Loading Pages...[/B]',remaining_display); 
		dialogWait.close(); del dialogWait
	### \/ Catching Items.
	html=nolines(messupText(html.replace("&nbsp;",""),True,True)); 
	deb("length of all pages",str(len(html))); 
	###s='src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>.+?<a href="http://[A-Za-z0-9\.]*/channels\?lang=\d*">([A-Za-z]*)</a>\s*</li>'; 
	###s='src=".+?" alt=".+?
	##s='<img width=".+?" height=".+?" src="(http://snapshots.ilive.to/snapshots/[0-9a-zA-Z]+_snapshot.[jpg|png]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>.+?'; 
	##s+='<span class="viewers">(.*?)</span>\s*'; s+='<span class="totalviews">(.*?)</span><br/>\s*'; 
	##s+='<a href="http://[A-Za-z0-9\.]*/channels/[A-Za-z\s]*">([A-Za-z0-9\s]*)</a>\s*'; 
	##s+='<a href="http://[A-Za-z0-9\.]*/channels\?lang=\d*">([A-Za-z0-9\s]*)</a>\s*</li>'; 
	#'src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>'
	s='<noscript><img width="\d+" height="\d+" src="(\D+://snapshots.(?:ilive.to|streamlive.to)?/snapshots/[0-9a-zA-Z]+_snapshot.jpg)" alt=".+?"\s*/></noscript>\s*</a>\s*'; 
	s+='<a href="(\D+://www.(?:ilive.to|streamlive.to)?/(?:view|view-channel|watch-channel|%s)?/\d+/.+?)"><strong>\s*(.+?)\s*</strong></a><br/>\s*'%UrlTAG; 
	s+='<span class="viewers">([0-9\,]+)</span>\s*'; 
	s+='<span class="totalviews">([0-9\,]+)</span><br/>\s*'; 
	s+='<a href="\D+://www.(?:ilive.to|streamlive.to)?/channels/.+?">([A-Za-z0-9\s]*)</a>\s*'; 
	s+='<a href="\D+://www.(?:ilive.to|streamlive.to)?/channels\?lang=\d*">([A-Za-z0-9\s]*)</a>\s*</li'; 
	#debob(html); 
	match=re.compile(s).findall(html); ItemCount=len(match); debob(match); 
	
	#match=sorted(match, key=lambda item: item[2], reverse=False)
	#match=sorted(match, key=lambda item: item[3], reverse=False)
	### \/ Links
	for thumb,url,name,iViewers,iTotalViews,Category,lang in match:
		unCacheAnImage(thumb); 
		pars={'mode':'iLivePlay','site':site,'section':section,'title':name,'url':url,'fanart':thumb,'img':thumb,'link':'99'}; 
		PlotD=cFL("[CR]Language: "+lang+"[CR]Category: "+Category+"[CR]Viewers: "+iViewers+"[CR]TotalViews: "+iTotalViews,"tan"); 
		#debob(pars); 
		try: _addon.add_directory(pars,{'title':name+'  ['+cFL(lang,colors['6'])+']','plot':PlotD},is_folder=False,fanart=thumb,img=thumb,total_items=ItemCount)
		except: pass
	
	###
	set_view('movies',view_mode=addst('movies-view')); 
	#set_view('tvshows',view_mode=addst('tvshows-view')); 
	#set_view('list',view_mode=addst('default-view')); 
	eod(); 
def iLiveBrowseLIVE(channel='',iLive_Sort='',iLive_Language='',iLive_category='',search=''):
	iLive_category=channel
	if len(iLive_Sort)==0: iLive_Sort="0"
	##channel=channel.replace(" ","%20"); 
	#### \/ Catching the first page.
	##if len(search) > 0: tUrl="http://www.ilive.to/channels/?q=%s"%search
	##else: tUrl="http://www.ilive.to/channels/"+channel.replace(" ","%20")+"?sort="+iLive_Sort+"&lang="+iLive_Language; 
	##else: 
	##tUrl="http://www.ilive.to/api/live.xml"; tUrl="http://www.streamlive.to/api/live.xml"; 
	#ApiLiveDomain=addst('DefaultApiLiveList','Default')
	tUrl=doMain+"api/live.xml"; 
	#if   ApiLiveDomain=='ilive.to': tUrl="http://www.ilive.to/api/live.xml"; 
	#elif ApiLiveDomain=='streamlive.to': tUrl="http://www.streamlive.to/api/live.xml"; 
	#else: tUrl="http://www.streamlive.to/api/live.xml"; 
	#if   ApiLiveDomain=='ilive.to': headers={'Referer':'http://www.ilive.to/'}; 
	#elif ApiLiveDomain=='streamlive.to': headers={'Referer':'http://www.streamlive.to/'}; 
	#else: headers={'Referer':'http://www.streamlive.to/'}; 
	deb("url",tUrl); 
	html=nURL(tUrl,headers=headers); deb("length of remote xml",str(len(html))); 
	LocalXML=os.path.join(_addonPath,'live.xml')
	if len(html) > 20:
		try: _SaveFile(LocalXML,html)
		except: pass
	elif isFile(LocalXML):
		deb("Faild to load Remote File","Attempting to load local file."); myNote("Faild to load Remote File","Attempting to load local file."); 
		try: html=_OpenFile(LocalXML)
		except: html=''
		deb("length of local xml",str(len(html))); 
		if len(html) < 20:
			deb("Faild to load Remote File","Unable to locate local file."); myNote("Faild to load Remote File","Unable to locate local file."); 
	else: 
		deb("Faild to load Remote File","Unable to locate local file."); myNote("Faild to load Remote File","Unable to locate local file."); 
		pass
	if ('/api/' in tUrl) and ('.xml' in tUrl):
		iLive_Language=LanguageNoToNa(iLive_Language)
		debob({'iLive_Language':iLive_Language,'iLive_category':iLive_category,'search':search}); 
		if '</channels>' in html:
			html=nolines(html).split('</channels>')[0]
			if '<channels>' in html:
				html=html.split('<channels>')[1]; html=html.replace('</channel><channel>','</channel>\n\r<channel>').replace('</channel>','</channel\n\r>'); deb('Length of HTML',str(len(html))); #debob(html); 
				##  <channel><name>SKY S</name><url> http://   www.  ilive.to/view/68276 </url><image> http://snapshots.ilive.to/snapshots/wf9hh_snapshot.jpg</image><category>Live S</category><language>Engli</language><views>116.5</views></channel>
				#s="<channel><name>(.+?)</name><url>(http://(?:www.)?(?:ilive.to|streamlive.to)?/view/(\d+))</url><image>(http://snapshots.\D+.\D+/snapshots/(.+?)_snapshot.jpg)</image><category>(.+?)</category><language>(.*?)</language><views>(.*?)</views></channel"; 
				s="<channel><name>(.+?)</name><url>(http://(?:www.)?(?:ilive.to|streamlive.to)?/(?:view|\D+-channel|%s)?/(\d+))</url><image>(http://snapshots.\D+.\D+/snapshots/(.+?)_snapshot.jpg)</image><category>(.+?)</category><language>(.*?)</language><views>(.*?)</views></channel"%UrlTAG; 
				try: match=re.compile(s).findall(html); 
				except: match=[]
				ItemCount=len(match); deb('number of matches',str(ItemCount)); #debob(match); 
				if ItemCount > 0:
					match=sorted(match,key=lambda i:(i[5],i[0],i[6],i[7]),reverse=False)
					for (ChName,ChUrl,ChId,ChImg,ChImgId,ChCat,ChLang,ChViews) in match:
						#debob({'ChName':ChName,'ChUrl':ChUrl,'ChId':ChId,'ChImg':ChImg,'ChImgId':ChImgId,'ChCat':ChCat,'ChLang':ChLang,'ChViews':ChViews})
						if (len(search) > 0) and (not search.lower() in ChName.lower()): pass
						elif (len(iLive_Language) > 0) and (not iLive_Language.lower()==ChLang.lower()): pass
						elif (len(iLive_category) > 0) and (not iLive_category.lower()==ChCat.lower()): pass
						else:
							debob({'ChName':ChName,'ChUrl':ChUrl,'ChId':ChId,'ChImg':ChImg,'ChImgId':ChImgId,'ChCat':ChCat,'ChLang':ChLang,'ChViews':ChViews})
							contextMenuItems=[]; unCacheAnImage(ChImg); 
							pars={'mode':'iLivePlay','site':site,'section':section,'title':ChName,'url':ChUrl,'fanart':ChImg,'img':ChImg,'link':'99'}; 
							pars0={'mode':'iLivePlay','site':site,'section':section,'title':ChName,'url':ChUrl,'fanart':ChImg,'img':ChImg,'link':'0'}; 
							pars1={'mode':'iLivePlay','site':site,'section':section,'title':ChName,'url':ChUrl,'fanart':ChImg,'img':ChImg,'link':'1'}; 
							pars2={'mode':'iLivePlay','site':site,'section':section,'title':ChName,'url':ChUrl,'fanart':ChImg,'img':ChImg,'link':'2'}; 
							PlotD=cFL("[CR]Language: "+ChLang+"[CR]Category: "+ChCat+"[CR]Views: "+ChViews,"tan"); 
							contextMenuItems.append(('Channel Information','XBMC.Action(Info)'))
							#contextMenuItems.append(('Play [HLS]' ,'XBMC.Container.Update(%s)'%_addon.build_plugin_url(pars0) ))
							#contextMenuItems.append(('Play [RTMP]','XBMC.Container.Update(%s)'%_addon.build_plugin_url(pars1) ))
							#contextMenuItems.append(('Play [RTSP]','XBMC.Container.Update(%s)'%_addon.build_plugin_url(pars2) ))
							contextMenuItems.append(('Play [HLS]' ,'XBMC.RunPlugin(%s)'%_addon.build_plugin_url(pars0) ))
							contextMenuItems.append(('Play [RTMP]','XBMC.RunPlugin(%s)'%_addon.build_plugin_url(pars1) ))
							contextMenuItems.append(('Play [RTSP]','XBMC.RunPlugin(%s)'%_addon.build_plugin_url(pars2) ))
							
							try: _addon.add_directory(pars,{'title':ChName+'  ['+cFL(ChLang,colors['6'])+']','plot':PlotD},is_folder=False,fanart=ChImg,img=ChImg,total_items=ItemCount,contextmenu_items=contextMenuItems,context_replace=False)
							except: pass
	else:
		### \/ Catching the rest of the pages.
		if '<p align="center" class="pages"><strong>Page: </strong>' in html:
			phtml=html.split('<p align="center" class="pages"><strong>Page: </strong>')[1].split('</span></p>')[0]; deb("length of phtml",str(len(phtml))); 
			try: ppages=re.compile('<a href="(http://www.(?:ilive.to|streamlive.to)?/channels/.+?)">\s*(\d+)\s*</a>').findall(phtml)
			except: ppages=[]
			deb("number of pages",str(len(ppages)+1)); debob(ppages); 
			dialogWait=xbmcgui.DialogProgress(); loaded=1; ptotal=len(ppages)+1; ret=dialogWait.create('Please wait...'); 
			percent=(loaded * 100)/ptotal; remaining_display='[B]Page '+str(loaded)+' of '+str(ptotal)+'[/B].'; dialogWait.update(percent,'[B]Loading Pages...[/B]',remaining_display); 
			for (ppage,pname) in ppages: 
				time.sleep(1); html+=nURL(ppage.replace(" ","%20")); 
				loaded=loaded+1; percent=(loaded * 100)/ptotal; remaining_display='[B]Page '+str(loaded)+' of '+str(ptotal)+'[/B].'; dialogWait.update(percent,'[B]Loading Pages...[/B]',remaining_display); 
			dialogWait.close(); del dialogWait
		### \/ Catching Items.
		html=nolines(messupText(html.replace("&nbsp;",""),True,True)); 
		deb("length of all pages",str(len(html))); 
		s='<noscript><img width="\d+" height="\d+" src="(http://snapshots.(?:ilive.to|streamlive.to)?/snapshots/[0-9a-zA-Z]+_snapshot.jpg)" alt=".+?"\s*/></noscript>\s*</a>\s*\n*\s*'; 
		s+='<a href="(http://www.(?:ilive.to|streamlive.to)?/(?:view|\D+-channel|%s)?/\d+/.+?)"><strong>\s*(.+?)\s*</strong></a><br/>\s*'%UrlTAG; 
		s+='<span class="viewers">([0-9\,]+)</span>\s*'; 
		s+='<span class="totalviews">([0-9\,]+)</span><br/>\s*'; 
		s+='<a href="http://www.(?:ilive.to|streamlive.to)?/channels/.+?">([A-Za-z0-9\s]*)</a>\s*'; s+='<a href="http://www.(?:ilive.to|streamlive.to)?/channels\?lang=\d*">([A-Za-z0-9\s]*)</a>\s*</li>'; 
		#debob(html); 
		match=re.compile(s).findall(html); ItemCount=len(match); 
		debob(match); 
		#match=sorted(match, key=lambda item: item[2], reverse=False)
		#match=sorted(match, key=lambda item: item[3], reverse=False)
		### \/ Links
		for thumb,url,name,iViewers,iTotalViews,Category,lang in match:
			unCacheAnImage(thumb); 
			pars={'mode':'iLivePlay','site':site,'section':section,'title':name,'url':url,'fanart':thumb,'img':thumb}; 
			PlotD=cFL("[CR]Language: "+lang+"[CR]Category: "+Category+"[CR]Viewers: "+iViewers+"[CR]TotalViews: "+iTotalViews,"tan"); 
			#debob(pars); 
			try: _addon.add_directory(pars,{'title':name+'  ['+cFL(lang,colors['6'])+']','plot':PlotD},is_folder=False,fanart=thumb,img=thumb,total_items=ItemCount)
			except: pass
	###
	set_view('movies',view_mode=addst('movies-view')); 
	#set_view('tvshows',view_mode=addst('tvshows-view')); 
	#set_view('list',view_mode=addst('default-view')); 
	eod(); 
def SSortSet(SSort): addstv("iLive_Sort",SSort); eod(); DoA("Back"); 
def SSortMenu():
	sC1='section'; sC2='live'; iLL='SSortSet'; fS=fanartSite; iS=iconSite; BB=[]; 
	BB.append(("0","Default")); BB.append(("1","Current Viewers")); BB.append(("2","Total Views")); 
	for (ssort,name) in BB:
		_addon.add_directory({'sort':ssort,'mode':iLL,'site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	set_view('list',view_mode=addst('default-view')); eod(); 
def LanguageNoToNa(n='',a=''):
	n=str(n).lower()
	if n=='': n=addst("iLive_Language")
	if  (n=='') or (n=='all'): a=''
	elif n=='1': a='English'
	elif n=='2': a='Spanish'
	elif n=='3': a='Portuguese'
	elif n=='4': a='French'
	elif n=='5': a='German'
	elif n=='6': a='Russian'
	elif n=='7': a='Vietnamese'
	elif n=='8': a='Italian'
	elif n=='9': a='Filipino'
	elif n=='10': a='Thai'
	elif n=='11': a='Chinese'
	elif n=='12': a='Indian'
	elif n=='13': a='Japanese'
	elif n=='14': a='Greek'
	elif n=='15': a='Dutch'
	elif n=='16': a='Swedish'
	elif n=='17': a='Unidentified'
	elif n=='18': a='Korean'
	elif n=='19': a='Brazilian'
	elif n=='20': a='Indian'
	elif n=='21': a='Romanian'
	return a
def LanguageSet(Language): addstv("iLive_Language",Language); eod(); DoA("Back"); 
def LanguageMenu():
	sC1='section'; sC2='live'; iLL='LanguageSet'; fS=fanartSite; iS=iconSite; BB=[]; 
	BB.append(("","All")); BB.append(("1","English")); BB.append(("2","Spanish")); BB.append(("3","Portuguese")); BB.append(("4","French")); BB.append(("5","German")); BB.append(("6","Russian")); BB.append(("7","Vietnamese")); BB.append(("8","Italian")); BB.append(("9","Filipino")); BB.append(("10","Thai")); BB.append(("11","Chinese")); BB.append(("12","Indian")); BB.append(("13","Japanese")); BB.append(("14","Greek")); BB.append(("15","Dutch")); BB.append(("16","Swedish")); BB.append(("17","Unidentified")); BB.append(("18","Korean")); BB.append(("19","Brazilian")); BB.append(("20","Indian")); BB.append(("21","Romanian")); 
	for (language,name) in BB:
		_addon.add_directory({'language':language,'mode':iLL,'site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	set_view('list',view_mode=addst('default-view')); eod(); 
def UrlTagGetter():
	#try:
		TempHtml=nURL(doMain+'channels/'); debob(['doMain',doMain,str(len(TempHtml))]); 
		UrlTag=re.compile('\D+://www\.\D+live\.to/([A-Za-z\-]+)/\d+/').findall(TempHtml)[0]
		debob(['UrlTag',UrlTag]); 
		if (_debugging==True):
			myNote('Url Tag',UrlTag,image=iconSite)
		addstv('url-tag',UrlTag)
	#except: pass
def SectionMenu1(): #(site): #Old Menu
	sC1='section'; sC2='live'; iLL='iLiveList'; fS=fanartSite; iS=iconSite; 
	_addon.add_directory({'mode':'LanguageMenu','site':site,sC1:sC2},{'title':'* '+cFL_("Language",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	_addon.add_directory({'mode':'SSortMenu','site':site,sC1:sC2},{'title':'* '+cFL_("Sort By",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	###
	BB=[]; 
	BB.append(("","All")); BB.append(("Movies","Movies")); BB.append(("Entertainment","Entertainment")); BB.append(("Live Sport","Live Sport")); 
	BB.append(("Animation","Animation")); BB.append(("Lifecaster","Lifecaster")); BB.append(("Gaming","Gaming")); 
	BB.append(("General","General")); BB.append(("News","News")); BB.append(("Music","Music")); 
	BB.append(("Mobile","Mobile")); BB.append(("Family","Family")); BB.append(("Religion","Religion")); 
	BB.append(("Radio","Radio")); 
	for (channel,name) in BB: _addon.add_directory({'channel':channel,'mode':'iLiveBrowse','site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	###
	###
	#if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	###if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site,'endit':'false'},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'Search','site':site},{'title':cFL_('Search',colors['6'])},is_folder=True,fanart=fS,img=iS)
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	UrlTagGetter()
	#
	set_view('list',view_mode=addst('default-view')); eod()
def SectionMenu2(): #(site): #New Menu
	#iLiveBrowseLIVE(channel=addpr('channel',''),iLive_Sort=addst('iLive_Sort',''),iLive_Language=addst('iLive_Language',''),iLive_category=addst('iLive_Category',''),search=addst('search',''))
	sC1='section'; sC2='live'; iLL='iLiveList'; fS=fanartSite; iS=iconSite; 
	_addon.add_directory({'mode':'LanguageMenu','site':site,sC1:sC2},{'title':'* '+cFL_("Language",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	#_addon.add_directory({'mode':'SSortMenu','site':site,sC1:sC2},{'title':'* '+cFL_("Sort By",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	###
	BB=[]; 
	BB.append(("","All")); BB.append(("Movies","Movies")); BB.append(("Entertainment","Entertainment")); BB.append(("Live Sport","Live Sport")); 
	BB.append(("Animation","Animation")); BB.append(("Lifecaster","Lifecaster")); BB.append(("Gaming","Gaming")); 
	BB.append(("General","General")); BB.append(("News","News")); BB.append(("Music","Music")); 
	BB.append(("Mobile","Mobile")); BB.append(("Family","Family")); BB.append(("Religion","Religion")); 
	BB.append(("Radio","Radio")); 
	for (channel,name) in BB: _addon.add_directory({'channel':channel,'mode':'iLiveBrowseLIVE','site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	###
	###
	#if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	###if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site,'endit':'false'},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'SearchN','site':site},{'title':cFL_('Search',colors['6'])},is_folder=True,fanart=fS,img=iS)
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	UrlTagGetter()
	#
	set_view('list',view_mode=addst('default-view')); eod()
def SectionMenu(): #(site):
	#iLiveBrowseLIVE(channel=addpr('channel',''),iLive_Sort=addst('iLive_Sort',''),iLive_Language=addst('iLive_Language',''),iLive_category=addst('iLive_Category',''),search=addst('search',''))
	sC1='section'; sC2='live'; iLL='iLiveList'; fS=fanartSite; iS=iconSite; 
	_addon.add_directory({'mode':'SectionMenu2','site':site,sC1:sC2},{'title':'* '+cFL_("New Menu",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	_addon.add_directory({'mode':'SectionMenu1','site':site,sC1:sC2},{'title':'* '+cFL_("Old Menu",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	#
	set_view('list',view_mode=addst('default-view')); eod()


### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	deb('mode',mode); 
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='SectionMenu1'): 	SectionMenu1()
	elif (mode=='SectionMenu2'): 	SectionMenu2()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='About'): 				About()
	#elif (mode=='iLiveList'): 		iLiveList(addpr('title',''))
	elif (mode=='iLivePlay'): 		iLivePlay(addpr('title',''),url,thumbnail,LinkNo=addpr('link',''))
	elif (mode=='LanguageSet'): 	LanguageSet(addpr('language',''))
	elif (mode=='LanguageMenu'): 	LanguageMenu()
	elif (mode=='SSortSet'): 			SSortSet(addpr('sort',''))
	elif (mode=='SSortMenu'): 		SSortMenu()
	elif (mode=='iLiveBrowse'): 	iLiveBrowse(addpr('channel',''),addst('iLive_Sort',''),addst('iLive_Language',''))
	elif (mode=='iLiveBrowseLIVE'): 	iLiveBrowseLIVE(channel=addpr('channel',''),iLive_Sort=addst('iLive_Sort',''),iLive_Language=addst('iLive_Language',''),iLive_category=addpr('category',''),search=addpr('search',''))
	elif (mode=='Settings'): 			_addon.addon.openSettings() # Another method: _plugin.openSettings() ## Settings for this addon.
	elif (mode=='TextBoxFile'): 	TextBox2().load_file(url,addpr('title','')); #eod()
	elif (mode=='TextBoxUrl'):  	TextBox2().load_url(url,addpr('title','')); #eod()
	elif (mode=='Search'):				DoSearch(addpr('title',''))
	elif (mode=='SearchN'):				DoSearchLIVE(addpr('title',''))
	#elif (mode=='Search'): 				Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	### \/ Testing \/
	#elif (mode=='SearchLast'): 		
	#	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	#	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=True) #(site,section)
	#elif (mode=='SearchLast'): 		Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	else: myNote(header='Site:  "'+site+'"',msg=mode+' (mode) not found.'); import mMain
	#

mode_subcheck(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))
### ############################################################################################################
### ############################################################################################################
