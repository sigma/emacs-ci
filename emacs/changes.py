import os

from buildbot.changes.gitpoller import GitPoller

_pwd = os.path.dirname(__file__)
_pollers_root = os.path.join(_pwd, '..', '..', 'pollers')

class EmacsGitPoller(GitPoller):

    def __init__(self, repo, **kwargs):
        workdir = kwargs['workdir']
        if workdir is not None:
            kwargs['workdir'] = os.path.join(_pollers_root, workdir)
        GitPoller.__init__(self, repo, **kwargs)
