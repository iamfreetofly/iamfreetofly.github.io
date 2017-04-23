import re
import json
import urllib
import base64
import urlresolver
from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from resources.lib import common
from resources.lib.resolvers.__ga import GA
from urlresolver.resolver import UrlResolver, ResolverError
from urlresolver.plugins.lib import jsunpack

class Videobug(UrlResolver, GA):
    name = 'Videobug'
    host = 'videobug.se'
    domains = [host]

    def get_media_url(self, host, media_id):
        try:
            url = self.get_url(host, media_id)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            html = urlopen(req).read(2*1000*1000)
            streams = self._extract_streams(html)

            if not streams:
                raise ResolverError('Matches no template: ' + url)

            urls, labels = zip(*streams)

            for lab in labels:
                self.crowdsource_stream_name(lab)

            if len(labels) == 1:
                ind = 0
            else:
                heading = common.get_string(33100)
                ind = common.select(heading, labels)
                if ind < 0:
                    return False

            self.ga_track('stream select', labels[ind])

            url = urls[ind]
            if re.match(r'https?://redirector.googlevideo.com/', url):
                # Kodi can play directly, skip further resolve
                vidurl = url
            else:
                vidurl = urlresolver.resolve(url)

            if vidurl:
                self.ga_track('resolution success', labels[ind])
            else:
                self.ga_track('resolution failure', labels[ind])

            return vidurl

        except Exception as e:
            common.error('%s UrlResolver Exception: %s' % (self.name, e))
            common.popup(common.get_string(33300))
            self.ga_track('resolution exception: %s' % e)
            return False


    def get_url(self, host, media_id):
        if host != self.host:
            raise ResolverError('Invalid host: %s' % host)
        return 'http://%s/%s' % (host, media_id)

    url_pattern = re.compile(r'http://(%s)/(.*)' % re.escape(host))
    def get_host_and_id(self, url):
        r = re.match(self.url_pattern, url)
        try:
            return r.groups()
        except AttributeError:
            raise ResolverError('Invalid URL: %s' % url)

    def valid_url(self, web_url, host):
        r = re.match(self.url_pattern, web_url)
        return bool(r) or (host == self.host)

    def _extract_streams(self, html):
        '''Return list of streams (tuples (url, label))
        '''
        streams = [] # list of tuples (url, label)

        # unobscurify
        key = 5
        unobscurify = lambda s: urllib.unquote(''.join(chr(ord(c) - key) for c in urllib.unquote(s)))
        df = re.search(r"dF\(\\?'(.*)\\?'\)", html)
        if df:
            script_end = html.find('</script>', df.end())
            script_end = script_end + 9 if script_end > -1 else -1
            html = html[:script_end] + unobscurify(df.group(1)) + html[script_end:]

        # Allupload
        # http://videobug.se/vid-a/g2S5k34-MoC2293iUaa9Hw
        json_data = re.findall(r"json_data = '(.+)';", html)
        if json_data:
            strdecode_1 = lambda s: base64.b64decode(urllib.unquote(s)[::-1]) # no longer used?
            strdecode_2 = lambda s: base64.b64decode(urllib.unquote(s))
            try:
                hashes = json.loads(json_data[0])
                exclude = ['Subtitles', 'image', 'JS', 'ADV']
                videos = [h for h in hashes if h['s'] not in exclude]
                # try both decode methods
                try:
                    streams = [(strdecode_1(h['u']), h['s']) for h in videos]
                except Exception:
                    streams = [(strdecode_2(h['u']), h['s']) for h in videos]
            except Exception:
                pass

        # Picasaweb, Videobug
        # http://videobug.se/video/Wz3_oCoEYozRSbJFQo4fkjmuvR6LpsFHM-XZya5tuk6stTXWdUeyplq5vVvSm0Yr0MXPFUmLt2XqrbLMPnE_Mgz8NbhXMZ6XFDI4hj253Z7af95WQPPDlpizIuuUXavEJqB8-bXuKbx6HTCMb5p5FC90yg1kXJb6?
        if not streams:
            soup = BeautifulSoup(html, 'html5lib')
            player_func = re.compile(r'(player_[^\(]+)\(\);').match
            butts = soup.find_all('input', type='button', onclick=player_func)

            funcs = [player_func(b['onclick']).group(1) for b in butts]
            labels = [b['value'] for b in butts]

            try:
                func_bodies = [re.findall(r'%s\(\) *{(.+)};' % f, html)[0] for f in funcs]
                re_flash = re.compile(r"video *= *{[^:]+: *'(.*?)' *}")
                re_html5 = re.compile(r'<source.*?src=\"(.*?)\"')

                urls = [(re_flash.findall(fb) or re_html5.findall(fb))[0] for fb in func_bodies]
                streams = zip(urls, labels)
            except Exception:
                pass

        # http://videobug.se/vid-al/XNkjCT5pBx1YlndruYWdWg?&caption=-sgCv7BkuLZn41-ZxxJZhTsKYcZIDgJPGYNOuIpulC_4kcrZ9k3fGQabH5rDAKgiLMVJdesVZPs
        if not streams:
            vids = re.findall(r'''{ *file *: *strdecode\('(.+?)'\).*?label *: *"(.*?)"''', html)
            for cryptic_url, label in vids:
                url = base64.b64decode(urllib.unquote(cryptic_url)[::-1])
                streams.append((url, label))

        # http://videobug.se/vid/pVobcNozEWmTkarNnwX06w
        if not streams:
            if jsunpack.detect(html):
                unpacked = jsunpack.unpack(html)
                streams =  self._extract_streams(unpacked)

        # remove this hardcoded youtube link
        streams = [(u, l) for u, l in streams if u != 'https://www.youtube.com/watch?v=niBTIQIYlv8']

        return streams

    @classmethod
    def _is_enabled(cls):
        return True
