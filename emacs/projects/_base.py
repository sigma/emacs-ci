class EmacsProject(object):

    _project_name = ""

    def __init__(self, config, slaves):
        self._config = config
        self._slaves = slaves

    def dispatch(self):
        config = self._config

        config['slaves'].extend(self._slaves)
        config['builders'].extend(self.getBuilders())
        config['schedulers'].extend(self.getSchedulers())

        config['change_source'].extend(self.getPollers())


    def getPollers(self):
        return []

    def getSchedulers(self):
        return []

    def getBuilders(self):
        return []
