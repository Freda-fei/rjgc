from fabric.contrib.files import append,exists,sed
from fabric.api import env,local,run
import random
from fabric.context_managers import settings,hide

REPO_URL = "https://github.com/Freda-fei/rjgc.git" #(1)

def deploy():
    site_folder = f'/home/{env.user}/sites/47.243.21.204_8092' #(2)(3)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder) #，即使某个文件夹已经存在也不会报错
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)  # (2)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/notes/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["127.0.0.1", "localhost ","47.243.21.204"]')
    secret_key_file = source_folder + '/notes/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.9 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')
    


def _update_static_files(source_folder):
    run(
        f'cd {source_folder} '
        '&& ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_folder):
    run(
        f'cd {source_folder} '
        '&& ../virtualenv/bin/python manage.py migrate --noinput'
    )

if __name__ == "__main__":
    local('fab -f /path/fabfile.py deploy')