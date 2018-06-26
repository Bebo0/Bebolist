from django.db import models
# Create your models here.

# inherits from models.Model
# Classes that inherit from models.Model map to tables in the database
# They generate an "id" attribute, which will be a primary key column in the database
# Whenever something is added in this file, have to run python manage.py makemigrations
# To create a real database, need to run python manage.py migrate.
# To clean DB, run rm db.sqlite3 then python manage.py migrate --noinput

class List(models.Model):
	pass


class Item(models.Model):
	text = models.TextField(default='') # Django has other field types like IntegerField, CharField, DateField and so on. 
	#https://docs.djangoproject.com/en/1.11/ref/models/fields/
	list = models.ForeignKey(List, default=None)



