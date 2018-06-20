from django.shortcuts import render
from django.http import HttpResponse

# We need to officially register our 'lists' app with Django. Therefore, need to add 'lists' to
# INSTALLED_APPS in superlists/settings.py

# Create your views here.
def home_page(request):
	return render(request, 'home.html') # Django searches all app's directories to find a file named
										# templates then builds an HttpResonse based on content of file