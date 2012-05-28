import os
import yaml

from buildbot.buildslave import BuildSlave

_pwd = os.path.dirname(__file__)
_slaves_defs_dir = os.path.join(_pwd, '..', '..', 'slave-definitions')

def getSlaves():
    slaves = []
    cwd = os.getcwd()

    os.chdir(_slaves_defs_dir)
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')  # don't visit git directories
        if 'slave.yaml' in files:
            fpath = os.path.join(root, 'slave.yaml')
            f = file(fpath, 'r')
            d = yaml.load(f)
            if not d.has_key('password'):
                continue

            properties = {}
            slave_features = d.get('features', {})
            for key, val in slave_features.items():
                properties["slave/features/%s" % key] = val

            slave_binaries = d.get('binaries', {})
            for key, val in slave_binaries.items():
                properties["slave/binaries/%s" % key] = val

            slave_projects = d.get('projects', {})
            for key, val in slave_projects.items():
                properties["slave/projects/%s" % key] = val

            slaves.append(BuildSlave(root[2:].replace("/",":"), d['password'],
                                     properties=properties))

    os.chdir(cwd)
    return slaves
