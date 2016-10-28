import re
import urlresolver
from urllib2 import urlopen
from bs4 import BeautifulSoup
from resources.lib import common
from resources.lib.resolvers.__ga import GA
from urlresolver.resolver import UrlResolver, ResolverError

class Icdrama(UrlResolver, GA):
    name = 'Icdrama'
    host = 'icdrama.se'
    domains = [host]

    def get_media_url(self, host, media_id):
        try:
            html = urlopen(self.get_url(host, media_id)).read(2*1000*1000)
            soup = BeautifulSoup(html, 'html5lib')
            iframe = soup.find('iframe')
            url = iframe['src']
            vidurl = urlresolver.resolve(url)
            if vidurl:
                self.ga_track('resolution success')
            else:
                self.ga_track('resolution failure')
            return vidurl
        except Exception as e:
            common.error('%s UrlResolver Exception: %s' % (self.name, e))
            common.popup(common.get_string(33300))
            self.ga_track('resolution exception: %s' % e)
            return False

    def get_url(self, host, media_id):
        if host != self.host:
            raise ResolverError('Invalid host: %s' % host)
        return 'http://%s/%s.html' % (host, media_id)

    url_pattern = re.compile(r'http://(%s)/([^\.]+)\.html' % re.escape(host))
    def get_host_and_id(self, url):
        r = re.match(self.url_pattern, url)
        try:
            return r.groups()
        except AttributeError:
            raise ResolverError('Invalid URL: %s' % url)

    def valid_url(self, web_url, host):
        r = re.match(self.url_pattern, web_url)
        return bool(r) or (host == self.host)

    @classmethod
    def _is_enabled(cls):
        return True
