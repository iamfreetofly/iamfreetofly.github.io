import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import urlresolver
from contextlib import contextmanager
from os.path import abspath, dirname
from urlresolver.hmf import HostedMediaFile
from urllib import urlencode

_plugin_url = sys.argv[0]
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_dialog = xbmcgui.Dialog()

addon_name = _addon.getAddonInfo('name')
addon_id = _addon.getAddonInfo('id')
addon_version = _addon.getAddonInfo('version')
profile_dir = xbmc.translatePath(_addon.getAddonInfo('profile'))
get_string = _addon.getLocalizedString

def debug(s):
    xbmc.log(str(s), xbmc.LOGDEBUG)

def error(s):
    xbmc.log(str(s), xbmc.LOGERROR)

def action_url(action, **action_args):
    action_args['action'] = action
    for k, v in action_args.items():
        if type(v) is unicode:
            action_args[k] = v.encode('utf8')
    qs = urlencode(action_args)
    return _plugin_url + '?' + qs

def add_item(diritem):
    xbmcplugin.addDirectoryItem(**diritem)

def end_dir():
    xbmcplugin.endOfDirectory(_handle)

def diritem(label_or_stringid, url, image='', isfolder=True, context_menu=[]):
    if type(label_or_stringid) is int:
        label = get_string(label_or_stringid)
    else:
        label = label_or_stringid
    listitem = xbmcgui.ListItem(label, iconImage=image)
    listitem.addContextMenuItems(context_menu, replaceItems=True)
    # this is unpackable for xbmcplugin.addDirectoryItem
    return dict(
        handle   = _handle,
        url      = url,
        listitem = listitem,
        isFolder = isfolder
    )

def popup(s):
    try:
        # Gotham (13.0) and later
        _dialog.notification(addon_name, s)
    except AttributeError:
        _dialog.ok(addon_name, s)

def select(heading, options):
    return _dialog.select(heading, options)

def resolve(url):
    # import the resolvers so that urlresolvers pick them up
    import resources.lib.resolvers
    hmf = HostedMediaFile(url)
    return hmf.resolve()

def sleep(ms):
    xbmc.sleep(ms)

def back_dir():
    # back one directory
    xbmc.executebuiltin('Action(ParentDir)')

def refresh():
    # refresh directory
    xbmc.executebuiltin('Container.Refresh')

def run_plugin(url):
    xbmc.executebuiltin(run_plugin_builtin_url(url))

def run_plugin_builtin_url(url):
    return 'RunPlugin(%s)' % url

def input(heading):
    kb = xbmc.Keyboard(default='', heading=heading)
    kb.doModal()
    if kb.isConfirmed():
        return kb.getText()
    return None

@contextmanager
def busy_indicator():
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    try:
        yield
    finally:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
