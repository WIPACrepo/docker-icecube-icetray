import os
import re
import shutil
import subprocess
import glob
import argparse
from pprint import pprint
from datetime import datetime

image_name = 'icecube/icetray'

def get_date():
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

def call(*args, **kwargs):
    print('call: '+' '.join(str(a) for a in args), flush=True)
    subprocess.call(*args, **kwargs)

def check_call(*args, **kwargs):
    print('check_call: '+' '.join(str(a) for a in args), flush=True)
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
    if os.path.exists(dockerfile+'_'+target):
        dockerfile = dockerfile+'_'+target
    # grab cached image if available
    call(['docker', 'pull', full_tag])

    if target == 'base-devel':
        # update FROM image
        with open(dockerfile) as f:
            base_img = re.search('FROM (.*) as', f.read()).group(1)
        call(['docker', 'pull', base_img])

    # prepare icetray download
    if 'GITHUB_PASS' in os.environ:
        creds = os.environ['GITHUB_USER']+':'+os.environ['GITHUB_PASS']
    elif 'GITHUB_TOKEN' in os.environ:
        creds = os.environ['GITHUB_USER']+':'+os.environ['GITHUB_TOKEN']
    else:
        raise Exception('need to define GITHUB_PASS or GITHUB_TOKEN in env')
    icetray_dir = os.path.join(os.getcwd(), 'icetray')
    os.makedirs(icetray_dir)
    try:
        if target == 'install':
            check_call(['git', 'clone', 'https://'+creds+'@github.com/icecube/icetray.git', icetray_dir])
            branch = 'tags/'+version if version.startswith('V') else version
            check_call(['git', 'checkout', branch], cwd=icetray_dir)
        check_call(['docker', 'build', '-f', dockerfile, '--target', target, '-t', full_tag, '.'])
        check_call(['docker', 'push', full_tag])
    finally:
        if os.path.exists(icetray_dir):
            shutil.rmtree(icetray_dir)

def retag(old, new):
    full_tag_old = image_name+':'+old
    full_tag_new = image_name+':'+new
    check_call(['docker', 'tag', full_tag_old, full_tag_new])
    check_call(['docker', 'push', full_tag_new])

def get_tags(metaproject, version, base_os):
    dockerfiles = glob.glob(os.path.join(base_os, metaproject, version, 'Dockerfile*'))
    tags = []
    for dockerfile in dockerfiles:
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

    if version == 'stable' or version == 'main' or (metaproject == 'combo' and version > 'V01-02'):
        if 'base-devel' in tags and not skip(metaproject, version, 'base-devel', base_os):
            build_docker(metaproject, version, 'base-devel', base_os)
            retag(metaproject+'-'+version+'-base-devel-'+base_os, metaproject+'-'+version+'-base-devel')
            retag(metaproject+'-'+version+'-base-devel-'+base_os, metaproject+'-'+version+'-base-devel-'+base_os+'-'+date)

        if 'base' in tags and not skip(metaproject, version, 'base', base_os):
            build_docker(metaproject, version, 'base', base_os)
            retag(metaproject+'-'+version+'-base-'+base_os, metaproject+'-'+version+'-base')
            retag(metaproject+'-'+version+'-base-'+base_os, metaproject+'-'+version+'-base-'+base_os+'-'+date)

    if 'install' in tags and not skip(metaproject, version, 'install', base_os):
        build_docker(metaproject, version, 'install', base_os)
        retag(metaproject+'-'+version+'-install-'+base_os, metaproject+'-'+version+'-install')
        retag(metaproject+'-'+version+'-install-'+base_os, metaproject+'-'+version+'-install-'+base_os+'-'+date)

    if 'slim' in tags and not skip(metaproject, version, 'slim', base_os):
        build_docker(metaproject, version, 'slim', base_os)
        retag(metaproject+'-'+version+'-slim-'+base_os, metaproject+'-'+version+'-slim')
        retag(metaproject+'-'+version+'-slim-'+base_os, metaproject+'-'+version+'-slim-'+base_os+'-'+date)
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-slim-'+base_os, version+'-slim')

    if 'prod' in tags and not skip(metaproject, version, 'prod', base_os):
        build_docker(metaproject, version, 'prod', base_os)
        retag(metaproject+'-'+version+'-prod-'+base_os, metaproject+'-'+version+'-prod')
        retag(metaproject+'-'+version+'-prod-'+base_os, metaproject+'-'+version+'-prod-'+base_os+'-'+date)
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-prod-'+base_os, version+'-prod')

    if 'devel' in tags and not skip(metaproject, version, 'devel', base_os):
        build_docker(metaproject, version, 'devel', base_os)
        retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version+'-devel')
        retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version)
        retag(metaproject+'-'+version+'-devel-'+base_os, metaproject+'-'+version+'-devel-'+base_os+'-'+date)
        if metaproject == 'combo' and version == 'stable':
            retag(metaproject+'-'+version+'-devel-'+base_os, version+'-devel')
            retag(metaproject+'-'+version+'-devel-'+base_os, version)
            retag(metaproject+'-'+version+'-devel-'+base_os, 'latest')

    for t in tags:
        if 'cuda' in t or 'tensorflow' in t or 'icecube-ml' in t:
            if not skip(metaproject, version, t, base_os):
                build_docker(metaproject, version, t, base_os)
                retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-'+t)
                retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-'+t+'-'+base_os+'-'+date)
                if 'cuda' in t:
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-cuda')
                elif 'tensorflow' in t:
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-tensorflow')
                elif 'icecube-ml' in t:
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-ml')
                if metaproject == 'combo' and version == 'stable':

                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-'+t)
                    if 'cuda' in t:
                        retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-cuda')
                    elif 'tensorflow' in t:
                        retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-tensorflow')
                    elif 'icecube-ml' in t:
                        retag(metaproject+'-'+version+'-'+t+'-'+base_os, version+'-ml')
                    retag(metaproject+'-'+version+'-'+t+'-'+base_os, metaproject+'-'+version+'-'+t+'-'+base_os+'-'+date)

def main():
    parser = argparse.ArgumentParser()
    os_options = ['ubuntu18.04','ubuntu20.04']
    parser.add_argument('--os', action='append', choices=os_options, default=os_options)
    parser.add_argument('--metaproject', action='append')
    parser.add_argument('--version', action='append')
    parser.add_argument('--print-tags', action='store_true')
    args = parser.parse_args()
    for base_os in args.os:
        for metaproject in os.listdir(base_os):
            if (not args.metaproject) or metaproject in args.metaproject:
                for version in os.listdir(os.path.join(base_os, metaproject)):
                    if (not args.version) or version in args.version:
                        if args.print_tags:
                            print('now working on '+metaproject+'-'+version+'-XXX-'+base_os)
                            pprint(get_tags(metaproject, version, base_os))
                        else:
                            build_metaproject(metaproject, version, base_os)

if __name__ == '__main__':
    main()
