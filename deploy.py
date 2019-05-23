import os
import subprocess

image_name = 'icecube/icetray'


def call(*args, **kwargs):
    print('call: '+' '.join(str(a) for a in args))
    subprocess.call(*args, **kwargs)

def check_call(*args, **kwargs):
    print('check_call: '+' '.join(str(a) for a in args))
    subprocess.check_call(*args, **kwargs)


def build_docker(metaproject, version, target, base_os):
    tag = metaproject+'-'+version+'-'+target+'-'+base_os
    full_tag = image_name+':'+tag
    dockerfile = os.path.join(base_os, metaproject, version, 'Dockerfile')
    call(['docker', 'pull', full_tag])
    check_call(['docker', 'build', '-f', dockerfile, '--target', target, '-t', full_tag, '.'])
    check_call(['docker', 'push', full_tag])

def retag(old, new):
    full_tag_old = image_name+':'+old
    full_tag_new = image_name+':'+new
    check_call(['docker', 'tag', full_tag_old, full_tag_new])
    check_call(['docker', 'push', full_tag_new])

def build_metaproject(metaproject, version, base_os):
    print('now working on '+metaproject+'-'+version+'-XXX-'+base_os)

    build_docker(metaproject, version, 'base', base_os)

    build_docker(metaproject, version, 'slim', base_os)
    retag(metaproject+'-'+version+'-slim-'+base_os, metaproject+'-'+version+'-slim')
    if metaproject == 'combo' and version == 'stable':
        retag(metaproject+'-'+version+'-slim-'+base_os, version+'-slim')

    build_docker(metaproject, version, 'prod', base_os)
    retag(metaproject+'-'+version+'-prod-'+base_os, metaproject+'-'+version+'-prod')
    if metaproject == 'combo' and version == 'stable':
        retag(metaproject+'-'+version+'-prod-'+base_os, version+'-prod')

    build_docker(metaproject, version, 'devel', base_os)
    retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version+'-devel')
    retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version)
    if metaproject == 'combo' and version == 'stable':
        retag(metaproject+'-'+version+'-devel-'+base_os, version+'-devel')
        retag(metaproject+'-'+version+'-devel-'+base_os, version)
        retag(metaproject+'-'+version+'-devel-'+base_os, 'latest')

    build_docker(metaproject, version, 'cuda10.1', base_os)
    retag(metaproject+'-'+version+'-cuda10.1-'+base_os, metaproject+'-'+version+'-cuda10.1')
    retag(metaproject+'-'+version+'-cuda10.1-'+base_os, metaproject+'-'+version+'-cuda')
    if metaproject == 'combo' and version == 'stable':
        retag(metaproject+'-'+version+'-cuda10.1-'+base_os, version+'-cuda10.1')
        retag(metaproject+'-'+version+'-cuda10.1-'+base_os, version+'-cuda')


for base_os in ('ubuntu18.04',):
    for metaproject in os.listdir(base_os):
        for version in os.listdir(os.path.join(base_os, metaproject)):
            build_metaproject(metaproject, version, base_os)