from buildbot.config import BuilderConfig

class EmacsBuildConfig(dict):

    def __init__(self, projectName="Buildbot", projectURL="", slavePortnum=9901,
                 buildbotURL="http://localhost:8010",
                 db_url="sqlite:///state.sqlite"):
        self['slaves'] = []
        self['change_source'] = []
        self['schedulers'] = []
        self['builders'] = []
        self['status'] = []

        self['slavePortnum'] = slavePortnum
        self['projectName'] = projectName
        self['projectURL'] = projectURL
        self['buildbotURL'] = buildbotURL
        self['db_url'] = db_url

        self['mergeRequests'] = True

class EmacsBuilderConfig(BuilderConfig):

    def __init__(self, name, branch, slavenames=None, factory=None, category=None):
        BuilderConfig.__init__(self, name=name, slavenames=slavenames,
                               factory=factory, category=category)
        self.branch = branch
