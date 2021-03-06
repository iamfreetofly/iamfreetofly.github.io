"""
    URLResolver Addon for Kodi
    Copyright (C) 2016 t0mm0, tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# this is to add urlresolver's own lib to sys path because (sometimes) kodi
# crashes on update when an addon is dependent on itself
import os
import sys
import xbmcaddon
addon_path = xbmcaddon.Addon().getAddonInfo('path')
sys.path.insert(0, os.path.join(addon_path, 'lib'))

from urlresolver.lib import kodi
from urlresolver.lib import log_utils
from urlresolver.lib.url_dispatcher import URL_Dispatcher
url_dispatcher = URL_Dispatcher()

def __enum(**enums):
    return type('Enum', (), enums)

MODES = __enum(AUTH_RD='auth_rd', RESET_RD='reset_rd')

@url_dispatcher.register(MODES.AUTH_RD)
def auth_rd():
    kodi.close_all()
    from urlresolver.plugins import realdebrid
    if realdebrid.RealDebridResolver().authorize_resolver():
        kodi.notify(msg='Real-Debrid Resolver Authorized', duration=5000)

@url_dispatcher.register(MODES.RESET_RD)
def reset_rd():
    kodi.close_all()
    from urlresolver.plugins import realdebrid
    rd = realdebrid.RealDebridResolver()
    rd.reset_authorization()
    kodi.notify(msg='Real-Debrid Authorization Reset', duration=5000)
    
def main(argv=None):
    if sys.argv: argv = sys.argv
    queries = kodi.parse_query(sys.argv[2])
    log_utils.log('Version: |%s| Queries: |%s|' % (kodi.get_version(), queries))
    log_utils.log('Args: |%s|' % (argv))

    # don't process params that don't match our url exactly. (e.g. plugin://plugin.video.1channel/extrafanart)
    plugin_url = 'plugin://%s/' % (kodi.get_id())
    if argv[0] != plugin_url:
        return

    mode = queries.get('mode', None)
    url_dispatcher.dispatch(mode, queries)

if __name__ == '__main__':
    sys.exit(main())
