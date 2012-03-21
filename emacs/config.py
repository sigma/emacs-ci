class BuildConfig(dict):

    def __init__(self, port=9901):
        self['slaves'] = []
        self['slavePortnum'] = port
        self['change_source'] = []
        self['schedulers'] = []
        self['builders'] = []
        self['status'] = []
