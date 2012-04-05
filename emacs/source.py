from buildbot.steps.source import Git

class DetachedGit(Git):
    """Git step, but ignoring information coming from pollers.  Useful for
    updating dependencies, that are unrelated to main project."""
    def startVC(self, branch, revision, patch):
        return Git.startVC(self, self.branch, None, None)
