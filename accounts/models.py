from django.db import models
from django.contrib import auth
import uuid

auth.signals.user_logged_in.disconnect(auth.models.update_last_login) # to prevent a weird Django error

class User(models.Model):
	email = models.EmailField(primary_key=True) # We only need this but Django complains about the underneath attributes
	# We make the emails the primary key instead of the auto generated IDs (1, 2, 3, ...)
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'email'
	is_anonymous = False
	is_authenticated = True

class Token(models.Model):
	email = models.EmailField()
	uid = models.CharField(default=uuid.uuid4, max_length=40) # Python comes with a module designed specifically
	# for generating unique IDs called "uuid" for "universally unique id". Better than using random.