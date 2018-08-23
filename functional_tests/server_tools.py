from fabric.api import run
from fabric.context_managers import settings, shell_env
import time
"""
This file allows us to run fab commands from within Python
"""
def _get_manage_dot_py(host):
	return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py'

def reset_database(host):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string=f'totoman@{host}'): # Sets the host string
		run(f'{manage_dot_py} flush --noinput') # We can call Fabric commands as if we're in a fabfile

def _get_server_env_vars(host):
	env_lines = run(f'cat ~/sites/{host}/.env').splitlines() # We extract and parse the server's current env vars from the .env file
	return dict(l.split('=') for l in env_lines if l)

def create_session_on_server(host, email):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string=f'totoman@{host}'):
		env_vars = _get_server_env_vars(host)
		with shell_env(**env_vars): # shell_env sets the environment for the next command
			
			session_key = run(f'{manage_dot_py} create_session {email}')
			session_key = session_key[1:] # Fixes weird ass bug. Took me 2 hours ffs
			return session_key.strip()

