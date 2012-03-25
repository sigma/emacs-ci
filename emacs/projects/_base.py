from itertools import product
from ..config import EmacsBuilderConfig
from ..changes import EmacsGitPoller
from ..steps import EmacsCompile

from buildbot.changes import filter
from buildbot.process.factory import BuildFactory
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.steps.source import Git

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

    def validateFeature(self, proposed, expected):
        if callable(expected):
            return expected(proposed)
        return expected == proposed

    def getAssignments(self):
        keys = self._project_combinations.keys()
        values = self._project_combinations.values()

        assignments = []

        for combo in product(*values):
            combo_tag = dict(zip(keys, combo))
            slaves = []
            for slave in self._slaves:
                fits = True
                for key, val in zip(keys, combo):
                    if not slave.properties.has_key("slave/features/" + key):
                        fits = False
                        break
                    if not self.validateFeature(
                        slave.properties['slave/features/' + key], val):
                        fits = False
                        break
                if fits:
                    slaves.append(slave.slavename)
            if slaves:
                assignments.append((combo_tag, slaves))

        return assignments

class EmacsGitProject(EmacsProject):

    _project_git_repo = ""
    _project_git_branches = ""
    _project_poll_default = 300
    _project_stable_default = 10

    def getPollers(self):
        return [self.getBranchPoller(branch)
                for branch in self._project_git_branches]

    def getBranchPoller(self, branch):
        return EmacsGitPoller(self._project_git_repo, branch,
                              self._project_poll_default, self)

    def computeSchedulers(self):
        schedulers = []

        for branch in self._project_git_branches:
            schedulers.append(self.getBranchScheduler(branch))

        return schedulers

    def getBranchScheduler(self, branch):
        filt = filter.ChangeFilter(project=self._project_name,
                                   branch=branch,
                                   category=self._project_name)
        builders = [b.name for b in self.getBuilders()
                    if b.branch==branch]
        name = "%s:%s" % (self._project_name, branch)
        return SingleBranchScheduler(
            name=name,
            change_filter=filt,
            treeStableTimer=self._project_stable_default,
            builderNames=builders)

    def computeBuilders(self):
        builders = []

        assignments = self.getAssignments()

        for branch in self._project_git_branches:
            for combo, slaves in assignments:
                factory = self.getFactory(branch, combo)
                if not slaves or len(slaves) == 0:
                    continue
                name = "%s:%s:%s" % (self._project_name,
                                     branch,
                                     ":".join([str(v) for v in combo.values()]))
                builders.append(EmacsBuilderConfig(name=name,
                                                   branch=branch,
                                                   slavenames=slaves,
                                                   factory=factory,
                                                   category=self._project_name))

        return builders

    def getFactory(self, branch, combo):
        factory = BuildFactory()
        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch))
        factory.addStep(
            EmacsCompile(command=["make", "clean", "all"]))
        return factory
