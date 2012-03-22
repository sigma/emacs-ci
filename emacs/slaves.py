import os
import yaml

from buildbot.buildslave import BuildSlave

_pwd = os.path.dirname(__file__)
_slaves_defs_dir = os.path.join(_pwd, '..', '..', 'slave-definitions')

def getSlaves():
    slaves = []

    for s in os.listdir(_slaves_defs_dir):
        f = file(os.path.join(_slaves_defs_dir, s, 'slave.yaml'), 'r')
        d = yaml.load(f)
        if not d.has_key('name') or not d.has_key('password'):
            continue

        properties = {}
        if d.has_key('features'):
            properties['features'] = d['features']

        slaves.append(BuildSlave(d['name'], d['password'],
                                 properties=properties))

    return slaves
