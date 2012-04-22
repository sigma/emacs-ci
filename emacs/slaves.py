import os
import yaml

from buildbot.buildslave import BuildSlave

_pwd = os.path.dirname(__file__)
_slaves_defs_dir = os.path.join(_pwd, '..', '..', 'slave-definitions')

def getSlaves():
    slaves = []

    for s in os.listdir(_slaves_defs_dir):
        fpath = os.path.join(_slaves_defs_dir, s, 'slave.yaml')
        if os.path.exists(fpath):
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

            slaves.append(BuildSlave(s, d['password'],
                                     properties=properties))

    return slaves
