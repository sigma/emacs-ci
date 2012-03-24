from buildbot.steps.shell import Compile, Test
from buildbot.status.results import SUCCESS, WARNINGS, FAILURE
import re

class EmacsCompile(Compile):

    warningPattern="^Warning:.*"

class EmacsTest(Test):

    warningPattern="^Warning:.*"

    def evaluateCommand(self, cmd):
        # Get stdio, stripping pesky newlines etc.
        lines = map(
            lambda line : line.replace('\r\n','').replace('\r','').replace('\n',''),
            self.getLog('stdio').readlines()
            )

        total = 0
        passed = 0
        failed = 0
        warnings = 0
        rc = SUCCESS
        if cmd.rc > 0:
            rc = FAILURE

        wre = self.warningPattern
        if isinstance(wre, str):
            wre = re.compile(wre)

        for line in lines:
            if line.startswith("   passed  "):
                passed += 1
                total += 1
            elif line.startswith("   FAILED  "):
                failed += 1
                total += 1
                rc = FAILURE
            elif wre.search(line):
                warnings += 1

        if rc == SUCCESS and warnings:
            rc = WARNINGS

        if total:
            self.setTestResults(total=total, failed=failed, passed=passed)

        return rc
