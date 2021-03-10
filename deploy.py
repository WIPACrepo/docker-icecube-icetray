import os
import subprocess
from datetime import datetime

image_name = 'icecube/icetray'

def get_date():
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

def call(*args, **kwargs):
    print('call: '+' '.join(str(a) for a in args))
    subprocess.call(*args, **kwargs)

def check_call(*args, **kwargs):
    print('check_call: '+' '.join(str(a) for a in args))
    subprocess.check_call(*args, **kwargs)

def skip(metaproject, version, target, base_os):
    if not version.startswith('V'):
        return False
    tag = metaproject+'-'+version+'-'+target+'-'+base_os
    try:
        check_call(['wget','-q','-O','-','https://hub.docker.com/v2/repositories/'+image_name+'/tags/'+tag])
    except Exception:
        return False
    return True

def build_docker(metaproject, version, target, base_os):
    tag = metaproject+'-'+version+'-'+target+'-'+base_os
    full_tag = image_name+':'+tag
    dockerfile = os.path.join(base_os, metaproject, version, 'Dockerfile')
    call(['docker', 'pull', full_tag])
    creds = os.environ['GITHUB_USER']+':'+os.environ['GITHUB_PASS']
    icetray_dir = os.path.join(os.getcwd(), 'icetray')
    os.makedirs(icetray_dir)
    check_call(['git', 'clone', 'https://'+creds+'@github.com/icecube/icetray.git', icetray_dir])
    try:
        branch = 'tags/'+version if version.startswith('V') else version
        check_call(['git', 'checkout', branch], cwd=icetray_dir)
        check_call(['docker', 'build', '--pull', '-f', dockerfile, '--target', target, '-t', full_tag, '.'])
        check_call(['docker', 'push', full_tag])
    finally:
        shutil.rmtree(icetray_dir)

def retag(old, new):
    full_tag_old = image_name+':'+old
    full_tag_new = image_name+':'+new
    check_call(['docker', 'tag', full_tag_old, full_tag_new])
    check_call(['docker', 'push', full_tag_new])

def get_tags(metaproject, version, base_os):
    dockerfile = os.path.join(base_os, metaproject, version, 'Dockerfile')
    tags = []
    with open(dockerfile) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[0].lower() == 'from' and parts[2].lower() == 'as':
                tags.append(parts[-1])
    return tags

def build_metaproject(metaproject, version, base_os):
    print('now working on '+metaproject+'-'+version+'-XXX-'+base_os)

    date = get_date()

    tags = get_tags(metaproject, version, base_os)

    if 'install' in tags and not skip(metaproject, version, 'install', base_os):
        build_docker(metaproject, version, 'install', base_os)
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-install-'+base_os, metaproject+'-'+version+'-install-'+base_os+'-'+date)

    if 'slim' in tags and not skip(metaproject, version, 'slim', base_os):
        build_docker(metaproject, version, 'slim', base_os)
        retag(metaproject+'-'+version+'-slim-'+base_os, metaproject+'-'+version+'-slim')
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-slim-'+base_os, version+'-slim')
            retag(metaproject+'-'+version+'-slim-'+base_os, metaproject+'-'+version+'-slim-'+base_os+'-'+date)

    if 'prod' in tags and not skip(metaproject, version, 'prod', base_os):
        build_docker(metaproject, version, 'prod', base_os)
        retag(metaproject+'-'+version+'-prod-'+base_os, metaproject+'-'+version+'-prod')
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-prod-'+base_os, version+'-prod')
            retag(metaproject+'-'+version+'-prod-'+base_os, metaproject+'-'+version+'-prod-'+base_os+'-'+date)

    if 'devel' in tags and not skip(metaproject, version, 'devel', base_os):
        build_docker(metaproject, version, 'devel', base_os)
        retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version+'-devel')
        retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version)
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-devel-'+base_os, version+'-devel')
            retag(metaproject+'-'+version+'-devel-'+base_os, version)
            retag(metaproject+'-'+version+'-devel-'+base_os, 'latest')
            retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version+'-devel-'+base_os+'-'+date)

    for t in tags:
        if 'cuda' in t or 'tensorflow' in t:
            if not skip(metaproject, version, t, base_os):
                build_docker(metaproject, version, t, base_os)
                retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-'+t)
                if 'cuda' in t:
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-cuda')
                elif 'tensorflow' in t:
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-tensorflow')
                if metaproject == 'combo' and version == 'stable':
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-'+t)
                    if 'cuda' in t:
                        retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-cuda')
                    elif 'tensorflow' in t:
                        retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-tensorflow')
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-'+t+'-'+base_os+'-'+date)


for base_os in ('ubuntu18.04','ubuntu20.04'):
    for metaproject in os.listdir(base_os):
        for version in os.listdir(os.path.join(base_os, metaproject)):
            build_metaproject(metaproject, version, base_os)