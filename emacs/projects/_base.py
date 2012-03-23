from itertools import product
from ..config import EmacsBuilderConfig

class EmacsProject(object):

    _project_name = ""
    _project_combinations = {}

    def __init__(self, config, slaves):
        self._config = config
        self._slaves = slaves
        self._builders = None
        self._schedulers = None
        self._pollers = None

    def dispatch(self):
        config = self._config

        config['slaves'].extend(self._slaves)
        config['builders'].extend(self.getBuilders())
        config['schedulers'].extend(self.getSchedulers())
        config['change_source'].extend(self.getPollers())

    def getPollers(self):
        if not self._pollers:
            self._pollers = self.computePollers()
        return self._pollers

    def computePollers(self):
        return []

    def getSchedulers(self):
        if not self._schedulers:
            self._schedulers = self.computeSchedulers()
        return self._schedulers

    def computeSchedulers(self):
        return []

    def getBuilders(self):
        if not self._builders:
            self._builders = self.computeBuilders()
        return self._builders

    def computeBuilders(self):
        return []

    def getAssignments(self):
        keys = self._project_combinations.keys()
        values = self._project_combinations.values()

        assignments = {}

        for combo in product(*values):
            combo_tag = ":".join(combo)
            assignments[combo_tag] = []
            for slave in self._slaves:
                fits = True
                for key, val in zip(keys, combo):
                    if not slave.properties['features'].has_key(key):
                        fits = False
                        break
                    if slave.properties['features'][key] != val:
                        fits = False
                        break
                if fits:
                    assignments[combo_tag].append(slave.slavename)

        return assignments

class EmacsGitProject(EmacsProject):

    _project_git_repo = ""
    _project_git_branches = ""

    def getPollers(self):
        return [self.getBranchPoller(branch)
                for branch in self._project_git_branches]

    def computeSchedulers(self):
        schedulers = []

        for branch in self._project_git_branches:
            schedulers.append(self.getBranchScheduler(branch))

        return schedulers

    def computeBuilders(self):
        builders = []

        assignments = self.getAssignments()

        for branch in self._project_git_branches:
            factory = self.getBranchFactory(branch)

            for combo, slaves in assignments.items():
                if not slaves or len(slaves) == 0:
                    continue
                name = "%s:%s:%s" % (self._project_name,
                                     branch, combo)
                builders.append(EmacsBuilderConfig(name=name,
                                                   branch=branch,
                                                   slavenames=slaves,
                                                   factory=factory,
                                                   category=self._project_name))

        return builders
