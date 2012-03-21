from ._base import EmacsProject
from ..changes import EmacsGitPoller

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.changes import filter

from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from ..steps import EmacsCompile
from buildbot.config import BuilderConfig

class MagitProject(EmacsProject):

    def getPollers(self):
        return [EmacsGitPoller(
                'git://github.com/magit/magit.git',
                workdir='magit-master',
                fetch_refspec='+refs/heads/master:refs/remotes/origin/master',
                branch='master', pollinterval=300)]

    def getSchedulers(self):
        return [SingleBranchScheduler(
                name="master",
                change_filter=filter.ChangeFilter(branch='master'),
                treeStableTimer=10,
                builderNames=["master:linux-oneiric"])]

    def getBuilders(self):
        build_master_factory = BuildFactory()
        build_master_factory.addStep(
            Git(repourl='git://github.com/magit/magit.git', mode='copy',
                branch="master"))
        build_master_factory.addStep(
            EmacsCompile(command=["make", "clean", "all"]))

        return [BuilderConfig(name="master:linux-oneiric",
                              slavenames=["magit:master:linux-oneiric"],
                              factory=build_master_factory)]
