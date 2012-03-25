from ._base import EmacsGitProject

from buildbot.process.properties import Property
from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.process.properties import WithProperties

from ..steps import EmacsCompile, EmacsTest
from ..versions import EmacsVersionIdentifier

class MockerProject(EmacsGitProject):

    _project_name = 'mocker'
    _project_combinations = {'os': ['lx-oneiric', 'osx-lion'],
                             'arch': ['x64'],
                             'emacs': [EmacsVersionIdentifier(kind="gnu",
                                                              version="24")]}

    _project_git_repo = 'git://github.com/sigma/mocker.el.git'
    _project_git_branches = ['master']

    def getFactory(self, branch, combo):
        factory = BuildFactory()
        _emacs = '%(slave/binaries/emacs:-emacs)s'
        _cargs = ["-batch", "-q", "-L", ".",
                  "-f", "batch-byte-compile",
                  "mocker.el"]
        _targs = ["-batch", "-q", "-L", ".",
                  "-l", "mocker-tests.el",
                  "-f", "ert-run-tests-batch-and-exit"]

        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch, logEnviron=False))
        factory.addStep(
            EmacsCompile(command=([WithProperties(_emacs)]+_cargs),
                         logEnviron=False))
        factory.addStep(
            EmacsTest(command=([WithProperties(_emacs)]+_targs),
                      logEnviron=False))
        return factory
