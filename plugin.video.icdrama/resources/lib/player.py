import xbmc
import xbmcgui

class _Player(xbmc.Player):
    pass
_player = _Player()

def play(url, title, image):
    li = xbmcgui.ListItem(title)
    li.setThumbnailImage(image)
    _player.play(url, li)
