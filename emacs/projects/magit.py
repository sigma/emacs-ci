from ._base import EmacsGitProject

from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.process.properties import WithProperties

from ..steps import EmacsCompile
from ..versions import EmacsVersionIdentifier

class MagitProject(EmacsGitProject):

    _project_name = 'magit'
    _project_combinations = {'os': ['lx-oneiric', 'osx-lion'],
                             'arch': ['x64'],
                             'emacs': [EmacsVersionIdentifier(kind="gnu",
                                                              version="24"),
                                       EmacsVersionIdentifier(kind="gnu",
                                                              version="23")]}

    _project_git_repo = 'git://github.com/magit/magit.git'
    _project_git_branches = ['maint', 'master', 'next']

    def getFactory(self, branch, combo):
        factory = BuildFactory()
        _emacs_prop = 'EMACS=%(slave/binaries/emacs:-emacs)s'
        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch, logEnviron=False))
        factory.addStep(
            EmacsCompile(command=["make",
                                  WithProperties(_emacs_prop),
                                  "clean", "all"],
                         logEnviron=False))
        return factory
