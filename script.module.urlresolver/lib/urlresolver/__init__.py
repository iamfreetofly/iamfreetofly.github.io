#    urlresolver XBMC Addon
#    Copyright (C) 2011 t0mm0
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
This module provides the main API for accessing the urlresolver features.

For most cases you probably want to use :func:`urlresolver.resolve` or 
:func:`urlresolver.choose_source`.

.. seealso::
	
	:class:`HostedMediaFile`


'''

import os
import common
import plugnplay
from types import HostedMediaFile
from plugnplay.interfaces import UrlResolver
from plugnplay.interfaces import PluginSettings
from plugnplay.interfaces import SiteAuth
import xbmcgui

#load all available plugins
plugnplay.set_plugin_dirs(common.plugins_path)
plugnplay.load_plugins()

def resolve(web_url):
    '''
    Resolve a web page to a media stream.
    
    It is usually as simple as::
        
        import urlresolver
        media_url = urlresolver.resolve(web_url) 
        
    where ``web_url`` is the address of a web page which is associated with a 
    media file and ``media_url`` is the direct URL to the media. 

    Behind the scenes, :mod:`urlresolver` will check each of the available 
    resolver plugins to see if they accept the ``web_url`` in priority order 
    (lowest priotity number first). When it finds a plugin willing to resolve 
    the URL, it passes the ``web_url`` to the plugin and returns the direct URL 
    to the media file, or ``False`` if it was not possible to resolve.
    
	.. seealso::
		
		:class:`HostedMediaFile`

    Args:
        web_url (str): A URL to a web page associated with a piece of media
        content.
        
    Returns:
        If the ``web_url`` could be resolved, a string containing the direct 
        URL to the media file, if not, returns ``False``.    
    '''
    source = HostedMediaFile(url=web_url)
    return source.resolve()

def filter_source_list(source_list):
    '''
    Takes a list of :class:`HostedMediaFile`s representing web pages that are 
    thought to be associated with media content. If no resolver plugins exist 
    to resolve a :class:`HostedMediaFile` to a link to a media file it is 
    removed from the list.
    
    Args:
        urls (list of :class:`HostedMediaFile`): A list of 
        :class:`HostedMediaFiles` representing web pages that are thought to be 
        associated with media content.
        
    Returns:
        The same list of :class:`HostedMediaFile` but with any that can't be 
        resolved by a resolver plugin removed.
    
    '''
    return [source for source in source_list if source]


def choose_source(sources):
    '''
    Given a list of :class:`HostedMediaFile` representing web pages that are 
    thought to be associated with media content this function checks which are 
    playable and if there are more than one it pops up a dialog box displaying 
    the choices.
    
    Example::
    
        sources = [HostedMediaFile(url='http://youtu.be/VIDEOID', title='Youtube [verified] (20 views)'),
                   HostedMediaFile(url='http://putlocker.com/file/VIDEOID', title='Putlocker (3 views)')]
		source = urlresolver.choose_source(sources)
		if source:
			stream_url = source.resolve()
			addon.resolve_url(stream_url)
		else:
			addon.resolve_url(False)

    Args:
        sources (list): A list of :class:`HostedMediaFile` representing web 
        pages that are thought to be associated with media content.
        
    Returns:
        The chosen :class:`HostedMediaFile` or ``False`` if the dialog is 
        cancelled or none of the :class:`HostedMediaFile` are resolvable.    
        
    '''
    #get rid of sources with no resolver plugin
    sources = filter_source_list(sources)
    
    #show dialog to choose source
    if len(sources) > 1:
        dialog = xbmcgui.Dialog()
        titles = []
        for source in sources:
            titles.append(source.title)
        index = dialog.select('Choose your stream', titles)
        if index > -1:
            return sources[index]
        else:
            return False
    
    #only one playable source so just play it
    elif len(sources) == 1:
        return sources[0]    
    
    #no playable sources available
    else:
        common.addon.log_error('no playable streams found')
        return False
    
        
def display_settings():
    '''
    Opens the settings dialog for :mod:`urlresolver` and its plugins.
    
    This can be called from your addon to provide access to global 
    :mod:`urlresolver` settings. Each resolver plugin is also capable of 
    exposing settings.
    
    .. note::
    
        All changes made to these setting by the user are global and will 
        affect any addon that uses :mod:`urlresolver` and its plugins.
    '''
    _update_settings_xml()
    common.addon.show_settings()
        
        
def _update_settings_xml():
    '''
    This function writes a new ``resources/settings.xml`` file which contains
    all settings for this addon and its plugins.
    '''
    try:
        try:
            os.makedirs(os.path.dirname(common.settings_file))
        except OSError:
            pass

        f = open(common.settings_file, 'w')
        try:
            f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write('<settings>\n')    
            for imp in PluginSettings.implementors():
                f.write('<category label="%s">\n' % imp.name)
                f.write(imp.get_settings_xml())
                f.write('</category>\n')
            f.write('</settings>')
        finally:
            f.close
    except IOError:
        common.addon.log_error('error writing ' + common.settings_file)


#make sure settings.xml is up to date
_update_settings_xml()
