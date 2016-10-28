import sys
import traceback
from os.path import relpath, dirname
from urlparse import parse_qsl
from urllib import unquote
from resources.lib import actions, common, ga

def main():
    common.debug(str(sys.argv))

    qs = sys.argv[2]
    kargs = dict((k, unquote(v))for k, v in parse_qsl(qs.lstrip('?')))

    action_name = kargs.pop('action', 'index') # popped
    if action_name in actions.actions:
        action_func = getattr(actions, action_name)
        action_func(**kargs)
    else:
        raise Exception('Invalid action: %s' % action_name)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        _, _, tb = sys.exc_info()
        here = dirname(__file__)
        for f, l, _, _ in  traceback.extract_tb(tb):
            if f.startswith(here):
                filename = relpath(f, here)
                line = l
        ga.exception('[%s] %s:%s' % (e, filename, line))
        raise
