from distutils.version import LooseVersion

class VersionIdentifier(object):

    def __init__(self, version=""):
        self._version = version

    def __call__(self, string):
        return self.isCompatibleVersionNumber(string)

    def isCompatibleVersionNumber(self, version):
        v = LooseVersion(version).version
        ref = LooseVersion(self._version).version
        try:
            for cpt in ref:
                head = v.pop(0)
                if cpt != head:
                    return False
            return True
        except:
            return False

    def __str__(self):
        return ""

class EmacsVersionIdentifier(VersionIdentifier):

    def __init__(self, kind="gnu", version="24"):
        VersionIdentifier.__init__(self, version=version)
        self._kind = kind

    def __call__(self, string):
        if self._kind == "gnu" and not string.startswith("GNU Emacs"):
            return False
        if self._kind == "x" and not string.startswith("XEmacs"):
            return False
        return self.isCompatibleVersionNumber(string.split()[-1])

    def __str__(self):
        return "%s-%s" % (self._kind, self._version)
