from ._base import EmacsGitProject

from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.process.properties import WithProperties

from ..steps import EmacsCompile, EmacsTest
from ..versions import EmacsVersionIdentifier
from ..utils import memoized

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

    _deps = [('mocker', 'git://github.com/sigma/mocker.el', 'master')]

    @memoized
    def getBasicFactory(self, branch):
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

    @memoized
    def getTestingFactory(self, branch):
        factory = BuildFactory()
        _emacs_prop = 'EMACS=%(slave/binaries/emacs:-emacs)s'
        _eflags = '-L ../mocker'

        for p, r, t in self._deps:
            factory.addStep(
                Git(repourl=r, branch=t,
                    workdir=p, logEnviron=False,
                    description=['updating %s' % (p)],
                    descriptionDone=['update %s' % (p)]))
        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch, logEnviron=False))
        factory.addStep(
            EmacsCompile(command=["make",
                                  WithProperties(_emacs_prop),
                                  "clean", "all"],
                         logEnviron=False))
        factory.addStep(
            EmacsTest(command=["make",
                               WithProperties(_emacs_prop),
                               "EFLAGS=%s" % (_eflags),
                               "test"],
                      logEnviron=False))
        return factory

    def getFactory(self, branch, combo):
        if not EmacsVersionIdentifier(kind="gnu", version="24")(combo['emacs']):
            return self.getBasicFactory(branch)

        if branch == "maint":
            return self.getBasicFactory(branch)

        return self.getTestingFactory(branch)
