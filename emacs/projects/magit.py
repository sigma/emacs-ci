from ._base import EmacsProject
from ..changes import EmacsGitPoller

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.changes import filter

from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from ..steps import EmacsCompile
from buildbot.config import BuilderConfig

class MagitProject(EmacsProject):

    _project_name = 'magit'

    MAGIT_GIT_REPO = 'git://github.com/magit/magit.git'
    MAGIT_GIT_BRANCHES = ['master']

    def getPollers(self):
        return [EmacsGitPoller(self.MAGIT_GIT_REPO, branch, 300, self)
                for branch in self.MAGIT_GIT_BRANCHES]

    def getSchedulers(self):
        return [SingleBranchScheduler(
                name="master",
                change_filter=filter.ChangeFilter(branch='master'),
                treeStableTimer=10,
                builderNames=["master:linux-oneiric"])]

    def getBuilders(self):
        build_master_factory = BuildFactory()
        build_master_factory.addStep(
            Git(repourl=self.MAGIT_GIT_REPO, mode='copy',
                branch="master"))
        build_master_factory.addStep(
            EmacsCompile(command=["make", "clean", "all"]))

        return [BuilderConfig(name="master:linux-oneiric",
                              slavenames=["magit:master:linux-oneiric"],
                              factory=build_master_factory)]
