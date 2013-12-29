'''
Megarelease urlresolver plugin
Copyright (C) 2013 Vinnydude

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re, os, time, xbmcgui, xbmc
import xbmcgui
from urlresolver import common
from lib import jsunpack

#SET ERROR_LOGO# THANKS TO VOINAGE, BSTRDMKR, ELDORADO
error_logo = os.path.join(common.addon_path, 'resources', 'images', 'redx.png')

net = Net()

class MegareleaseResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "megarelease"


    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, host, media_id):
        try:
            url = self.get_url(host, media_id)
            html = self.net.http_GET(url).content
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving Megarelease Link...')       
            dialog.update(0)
    
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)">', html)
            for name, value in r:
                data[name] = value
                data.update({'plugins_are_not_allowed_plus_ban':2})
            captchaimg = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
        
            if captchaimg:
                dialog.close()
                html = self.net.http_GET(captchaimg.group(1)).content
                part = re.search("challenge \: \\'(.+?)\\'", html)
                captchaimg = 'http://www.google.com/recaptcha/api/image?c='+part.group(1)
                img = xbmcgui.ControlImage(450,15,400,130,captchaimg)
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
        
                time.sleep(3)
        
                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()
        
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        solution = kb.getText()
                    elif userInput == '':
                        raise Exception ('You must enter text in the image to access video')
                else:
                    raise Exception ('Captcha Error')
                wdlg.close()
                dialog.close() 
                dialog.create('Resolving', 'Resolving Megarelease Link...') 
                dialog.update(50)
                data.update({'recaptcha_challenge_field':part.group(1),'recaptcha_response_field':solution})
                
            html = net.http_POST(url, data).content
            if re.findall('err', html):
                raise Exception('Wrong Captcha')
                

            sPattern =  '<script type=(?:"|\')text/javascript(?:"|\')>(eval\('
            sPattern += 'function\(p,a,c,k,e,d\)(?!.+player_ads.+).+np_vid.+?)'
            sPattern += '\s+?</script>'
            r = re.search(sPattern, html, re.DOTALL + re.IGNORECASE)
            if r:
                sJavascript = r.group(1)
                sUnpacked = jsunpack.unpack(sJavascript)
                sPattern  = '<embed id="np_vid"type="video/divx"src="(.+?)'
                sPattern += '"custommode='
                r = re.search(sPattern, sUnpacked)
                if r:
                    dialog.update(100)
                    dialog.close()
                    return r.group(1)
            else:
                num = re.compile('false\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|divx').findall(html)
                common.addon.log('NUM: '+str(num))
                for u1, u2, u3, u4 in num:
                    urlz = u4+'.'+u3+'.'+u2+'.'+u1
                pre = 'http://'+urlz+':182/d/'
                preb = re.compile('custommode\|(.+?)\|(.+?)\|182').findall(html)
                for ext, link in preb:
                    r = pre+link+'/video.'+ext
                    dialog.update(100)
                    dialog.close()
                    return r            
                                
        except Exception, e:
            common.addon.log('**** Megarelease Error occured: %s' % e)
            common.addon.show_small_popup('Error', str(e), 5000, '')
            return self.unresolvable(code=0, msg='Exception: %s' % e)

        
    def get_url(self, host, media_id):
        return 'http://megarelease.org/%s' % media_id 
        

    def get_host_and_id(self, url):
        r = re.search('//(.+?)/([0-9a-zA-Z]+)',url)
        if r:
            return r.groups()
        else:
            return False
        return('host', 'media_id')


    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false': return False
        return (re.match('http://(www.)?megarelease.org/' +
                         '[0-9A-Za-z]+', url) or
                         'megarelease' in host)
