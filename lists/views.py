from django.shortcuts import render
from django.http import HttpResponse

# We need to officially register our 'lists' app with Django. Therefore, need to add 'lists' to
# INSTALLED_APPS in superlists/settings.py

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {
		'new_item_text': request.POST.get('item_text', ''),  # render takes a dictionary as its third argument, which maps template variable names
		# to their values, so we can use it for the POST case as well as the normal case. Also, request.POST would create an error in the
		# case where we don't send a POST. Therefore, request.POST.get returns a default value '' when we're doing a normal GET request.
		})
	# return render(request, 'home.html') # Django searches all app's directories to find a file named
										# templates then builds an HttpResonse based on content of file