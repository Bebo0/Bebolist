from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

class Command(BaseCommand):

	"""
	
	handle will pick up an email address from the parser and then return
	the session key that we'll want to add to our broswer cookies, and the
	management command prints it out at the command line.

	Try it like this: python manage.py create_session a@b.com
	"""

	def add_arguments(self, parser):
		parser.add_argument('email')

	def handle(self, *args, **options):
		session_key = create_pre_authenticated_session(options['email'])
		self.stdout.write(session_key)

def create_pre_authenticated_session(email):
	user = User.objects.create(email=email)
	session = SessionStore()
	session[SESSION_KEY] = user.pk
	session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
	session.save()
	return session.session_key