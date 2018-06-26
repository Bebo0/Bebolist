from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item, List

# We need to officially register our 'lists' app with Django. Therefore, need to add 'lists' to
# INSTALLED_APPS in superlists/settings.py

# Create your views here.
def home_page(request):
	# if request.method == 'POST':
	# 	Item.objects.create(text=request.POST['item_text']) # creates a new Item, without needing to call .save()
	# 	return redirect('/lists/the-only-list-in-the-world') # https://en.wikipedia.org/wiki/Post/Redirect/Get
	

	return render(request, 'home.html')
		
	# return render(request, 'home.html', {
	# 	'new_item_text': new_item_text  # render takes a dictionary as its third argument, which maps template variable names
	# 	# to their values, so we can use it for the POST case as well as the normal case. Also, request.POST would create an error in the
	# 	# case where we don't send a POST. Therefore, request.POST.get returns a default value '' when we're doing a normal GET request.
	# 	})
	# return render(request, 'home.html') # Django searches all app's directories to find a file named
										# templates then builds an HttpResonse based on content of file

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	return render(request, 'list.html', {'list': list_})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')