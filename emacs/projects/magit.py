from ._base import EmacsGitProject
from ..changes import EmacsGitPoller

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.changes import filter

from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from ..steps import EmacsCompile

class MagitProject(EmacsGitProject):

    _project_name = 'magit'
    _project_combinations = {'os': ['lx-oneiric', 'osx-lion'],
                             'arch': ['x64']}

    _project_git_repo = 'git://github.com/magit/magit.git'
    _project_git_branches = ['maint', 'master', 'next']

    def getBranchPoller(self, branch):
        return EmacsGitPoller(self._project_git_repo, branch, 300, self)

    def getBranchScheduler(self, branch):
        filt = filter.ChangeFilter(branch=branch)
        builders = [b.name for b in self.getBuilders()
                    if b.branch==branch]
        name = "%s:%s" % (self._project_name, branch)
        return SingleBranchScheduler(name=name,
                                     change_filter=filt,
                                     treeStableTimer=10,
                                     builderNames=builders)

    def getBranchFactory(self, branch):
        factory = BuildFactory()
        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch))
        factory.addStep(
            EmacsCompile(command=["make", "clean", "all"]))
        return factory
