import sys
import json
import xbmc
import time
import urllib2
import xbmcgui
import platform
import functools
from urllib import urlencode
from urllib2 import urlopen
from threading import Thread
from contextlib import contextmanager
from resources.lib import common, config, settings

_build = xbmc.getInfoLabel('System.BuildVersion')
_version = _build.split()[0]
_xbmc_version = 'XBMC %s' % _version

_window = xbmcgui.Window()
_screen_size = '%sx%s' % (_window.getWidth(), _window.getHeight())
_default_ua = 'Python-urllib/%s' % urllib2.__version__

def _gen_ua():
    ua = _default_ua

    # windows
    try:
        major, minor = sys.getwindowsversion()[:2]
        return ua + ' (Windows NT %s.%s)' % (major, minor)
    except AttributeError:
        pass

    # mac
    if 'darwin' in sys.platform:
        version = '_'.join(platform.mac_ver()[1])
        version = '' if version == '__' else ' '+version
        return ua + ' (Mac OS X%s)' % version

    # unix
    ua += ' (Linux %s)' % platform.machine()
    dist = '/'.join(platform.linux_distribution()[:2])
    if dist != '/':
        ua += ' ' + dist
    return ua

try:
    _user_agent = _gen_ua()
except Exception as e:
    common.error('Something went wrong when constructing user agent: %s' % e)
    _user_agent = _default_ua


_common = dict(
    v    = 1,
    tid  = config.tracking_id,
    cid  = settings.client_id,
    ua   = _user_agent,
    sr   = _screen_size,
    ul   = xbmc.getLanguage(xbmc.ENGLISH_NAME),
    an   = common.addon_name,
    aid  = common.addon_id,
    av   = common.addon_version,
    aiid = _xbmc_version
)


_ga_url = 'https://www.google-analytics.com/collect'
def _send(payload):
    if not settings.allow_ga:
        return

    data = payload.copy()
    data.update(_common)
    for k, v in data.items():
        if type(v) is unicode:
            data[k] = v.encode('utf8')
    data_str = urlencode(data)

    try:
        common.debug('GA: %s' % json.dumps(data, indent=4))
        req = urlopen(_ga_url, data_str)
        code = req.getcode()
        if code > 399:
            common.error('GA status code %s' % code)
        else:
            common.debug('Successful GA')
    except Exception as e:
        common.error('Failed to request GA: %s' % e)
        # no need to re-raise


def _async_send(payload):
    t = Thread(target=_send, args=(payload,))
    t.start()


def event(category, action, label=None):
    payload = dict(t='event', ec=category, ea=action)
    if label:
        payload['el'] = label
    _async_send(payload)


def exception(description):
    payload = dict(t='exception', exd=description)
    _async_send(payload)


def timing(category, variable, time):
    '''`time` in ms
    '''
    payload = dict(t='timing', utc=category, utv=variable, utt=time)
    _async_send(payload)


@contextmanager
def log_time(category, variable):
    a = time.time()
    yield
    b = time.time()
    timing(category, variable, int((b-a)*1000))
