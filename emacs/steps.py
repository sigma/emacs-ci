from buildbot.steps.shell import Compile

class EmacsCompile(Compile):

    warningPattern="^Warning:.*"
