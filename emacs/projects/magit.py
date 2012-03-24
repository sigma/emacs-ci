from ._base import EmacsGitProject

from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from ..steps import EmacsCompile

class MagitProject(EmacsGitProject):

    _project_name = 'magit'
    _project_combinations = {'os': ['lx-oneiric', 'osx-lion'],
                             'arch': ['x64']}

    _project_git_repo = 'git://github.com/magit/magit.git'
    _project_git_branches = ['maint', 'master', 'next']

    def getBranchFactory(self, branch):
        factory = BuildFactory()
        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch, logEnviron=False))
        factory.addStep(
            EmacsCompile(command=["make", "clean", "all"],
                         logEnviron=False))
        return factory
