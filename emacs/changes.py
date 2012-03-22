import os

from buildbot.changes.gitpoller import GitPoller

_pwd = os.path.dirname(__file__)
_pollers_root = os.path.join(_pwd, '..', '..', 'pollers')

class EmacsGitPoller(GitPoller):

    def __init__(self, repo, branch, interval, project):
        workdir = os.path.join(_pollers_root,
                               "%s-%s" % (project._project_name, branch))
        spec = '+refs/heads/%s:refs/remotes/origin/%s' % (branch, branch)
        GitPoller.__init__(self, repo,
                           category=project._project_name,
                           workdir=workdir,
                           fetch_refspec=spec,
                           branch=branch, pollinterval=interval)
