class EmacsProject(object):

    def __init__(self, config, slaves):
        self._config = config
        self._slaves = slaves

    def dispatch(self):
        config = self._config

        config['change_source'].extend(self.getPollers())
        config['schedulers'].extend(self.getSchedulers())
        config['builders'].extend(self.getBuilders())

        config['slaves'].extend(self._slaves)

    def getPollers(self):
        return []

    def getSchedulers(self):
        return []

    def getBuilders(self):
        return []
