import random
from fabric.contrib.files import append, exists
from fabric.api import sudo, cd, env, local, run

import os
REPO_URL = 'https://github.com/Bebo0/TDD-Python-Web-Dev.git'

def deploy():
	use_sudo=True
	site_folder = f'/home/{env.user}/sites/{env.host}'
	sudo(f'mkdir -p {site_folder}')
	with cd(site_folder):
		_get_latest_source()
		_update_virtualenv()
		_create_or_update_dotenv()
		_update_static_files()
		_update_database()

def _get_latest_source():
	if exists('.git'):
		sudo('git fetch')
	else:
		sudo(f'git clone {REPO_URL} .')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	sudo(f'git reset --hard {current_commit}' )

def _update_virtualenv():
	if not exists('virtualenv/bin/pip'):
		sudo(f'python3.6 -m venv virtualenv')
	sudo('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
	append('.env', 'DJANGO_DEBUG_FALSE=y', use_sudo=True) # adds this to file if it doesn't already exist
	append('.env', f'SITENAME={env.host}', use_sudo=True)
	current_contents = sudo('cat .env')
	if 'DJANGO_SECRET_KEY' not in current_contents:
		new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
		append('.env', f'DJANGO_SECRET_KEY={new_secret}', use_sudo=True)
	email_password = os.environ['EMAIL_PASSWORD']
	append('env', f'EMAIL_PASSWORD={email_password}')

def _update_static_files():
	sudo('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
	sudo('./virtualenv/bin/python manage.py migrate --noinput')
