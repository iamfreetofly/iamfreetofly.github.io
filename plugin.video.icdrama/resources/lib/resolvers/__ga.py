from resources.lib import ga, cache

class GA(object):
    def ga_track(self, action, label=None):
        ga.event('URL resolution', '%s %s' % (self.name, action), label)

    def crowdsource_stream_name(self, stream_name):
        key = 'Crowdsource stream names : %s : %s' % (self.name, stream_name)
        try:
            cache.get(key)
        except KeyError:
            ga.event('Crowdsource stream names', self.name, stream_name)
            cache._put(key, '', 14400) # 10 days
