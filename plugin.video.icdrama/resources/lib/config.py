import base64
from os.path import join as pathjoin
from urlparse import urljoin
from resources.lib.common import diritem, action_url, profile_dir

base_url = 'http://icdrama.se'
cache_file = pathjoin(profile_dir, 'cache.pickle')
store_file = pathjoin(profile_dir, 'store.pickle')
tracking_id = base64.b64decode('VUEtNzgwNTA2NTItMg==')

def _rel2abs(relpath):
    return urljoin(base_url, relpath)

# the trailing forward slashes are necessary
# without it, page urls will be wrong (icdrama bug)
search_url = _rel2abs('/search/%s/')
index_items = [
    diritem(33011, action_url('saved_list')),
    diritem(33000, action_url('recent_updates', url=_rel2abs('/recently-updated/'))),
    diritem(33001, action_url('shows', url=_rel2abs('/hk-drama/'))),
    diritem(33002, action_url('shows', url=_rel2abs('/hk-movie/'))),
    diritem(33003, action_url('shows', url=_rel2abs('/hk-show/'))),
    diritem(33004, action_url('shows', url=_rel2abs('/chinese-drama/'))),
    diritem(33012, action_url('shows', url=_rel2abs('/chinese-drama-cantonesedub/'))),
    diritem(33005, action_url('shows', url=_rel2abs('/taiwanese-drama/'))),
    diritem(33013, action_url('shows', url=_rel2abs('/taiwanese-drama-cantonesedub/'))),
    diritem(33006, action_url('shows', url=_rel2abs('/korean-drama/'))),
    diritem(33014, action_url('shows', url=_rel2abs('/korean-drama-cantonesedub/'))),
    diritem(33015, action_url('shows', url=_rel2abs('/korean-drama-chinesesubtitles/'))),
    diritem(33007, action_url('shows', url=_rel2abs('/korean-show/'))),
    diritem(33008, action_url('shows', url=_rel2abs('/japanese-drama/'))),
    diritem(33016, action_url('shows', url=_rel2abs('/japanese-drama-cantonesedub/'))),
    diritem(33017, action_url('shows', url=_rel2abs('/japanese-drama-chinesesubtitles/'))),
    diritem(33009, action_url('shows', url=_rel2abs('/movies/'))),
    diritem(33010, action_url('search'))
]
