from ._base import EmacsGitProject

from buildbot.process.properties import Property
from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.process.properties import WithProperties

from ..steps import EmacsCompile, EmacsTest
from ..versions import EmacsVersionIdentifier
from ..source import DetachedGit

class GhProject(EmacsGitProject):

    _project_name = 'gh'
    _project_combinations = {'os': ['lx-oneiric', 'osx-lion'],
                             'arch': ['x64'],
                             'emacs': [EmacsVersionIdentifier(kind="gnu",
                                                              version="24")]}

    _project_git_repo = 'git://github.com/sigma/gh.el.git'
    _project_git_branches = ['master']

    _deps = [('pcache', 'git://github.com/sigma/pcache', 'master'),
             ('logito', 'git://github.com/sigma/logito', 'master'),
             ('mocker', 'git://github.com/sigma/mocker.el', 'master')]

    def getFactory(self, branch, combo):
        factory = BuildFactory()
        for p, r, t in self._deps:
            factory.addStep(
                DetachedGit(repourl=r, branch=t,
                            workdir=p, logEnviron=False,
                            description=['updating %s' % (p)],
                            descriptionDone=['update %s' % (p)]))
        _eflags = '-L ../pcache -L ../logito -L ../mocker'
        _emacs_prop = 'EMACS=%(slave/binaries/emacs:-emacs)s'
        factory.addStep(
            Git(repourl=self._project_git_repo, mode='copy',
                branch=branch, workdir=self._project_name, logEnviron=False,
                description=['updating', self._project_name],
                descriptionDone=['update', self._project_name]))
        factory.addStep(
            EmacsCompile(command=["make",
                                  WithProperties(_emacs_prop),
                                  "EFLAGS=%s" % (_eflags),
                                  "clean", "lisp"],
                         workdir=self._project_name, logEnviron=False))
        factory.addStep(
            EmacsTest(command=["make",
                               WithProperties(_emacs_prop),
                               "EFLAGS=%s" % (_eflags),
                               "test"],
                      workdir=self._project_name, logEnviron=False))
        return factory
