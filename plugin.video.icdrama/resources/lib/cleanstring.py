import ga
import re
from resources.lib import settings, common

def _ga_unseen_string(string_type, string):
    ga.event('Unseen String', string_type, string)

def show(eng, orig):
    eng = eng.strip(' -')
    orig = orig.strip(' -')
    if not orig:
        return eng
    elif not eng:
        return orig
    elif settings.title_lang == 1:
        return eng
    elif settings.title_lang == 2:
        return orig
    else: # settings.title_lang == 0
        return '%s - %s' % (eng, orig)

def page(page):
    match = re.match(r'Page (\d+)$', page)
    if match:
        page = common.get_string(33102) % match.group(1)
    elif re.match(u'\u00ab First$', page):
        page = common.get_string(33103)
    elif re.match(u'Last \u00bb$', page):
        page = common.get_string(33104)
    else:
        _ga_unseen_string('Page', page)
    return '[I][ %s ][/I]' % page

def version(version):
    if version == 'Watch online (Chinese Subtitles)':
        version = common.get_string(33110)
    elif version == 'Watch online (English Subtitles)':
        version = common.get_string(33111)
    elif version == 'Watch online (Cantonese)':
        version = common.get_string(33112)
    elif version == 'Watch online (Mandarin)':
        version = common.get_string(33113)
    else:
        _ga_unseen_string('Version', version)
        match = re.match(r'Watch online \(([^\)]+)\)$', version)
        if match:
            version = match.group(1)
    return version

def episode(episode):
    match = re.match(r'(\d+)(?: \[END\]|)$', episode)
    if match:
        return common.get_string(33105) % match.group(1)
    elif re.match(r'\d{4}-\d{2}-\d{2}', episode):
        return episode
    else:
        _ga_unseen_string('Episode', episode)
    return episode

def mirror(mirror, part):
    match = re.match(r'(?:Part ?|)(\d+)$', part)
    if match:
        part = common.get_string(33106) % match.group(1)
    elif part == 'Full':
        part = common.get_string(33107)
    else:
        _ga_unseen_string('Mirror', '%s - %s' % (mirror, part))
    return '[B]%s[/B] : %s' % (mirror, part)
