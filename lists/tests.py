from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

# functional test from users's persepctive
# unittest from programmer's perspective
# TestCase is an augmented version of unittest.TestCase
# run file using python manage.py test

# Django's main job is to decide what to do whe a user asks for a particular
# URL on our site. Django's workflow is like this:
#
# 1) An HTTP request comes in for a particular URL
# 2) Django uses some rules to decide which view function should deal with the
# request (referred to as resolving the URL)
# 3) The view function processes the request and returns an HTTP response
		

class HomePageTest(TestCase):

	# def test_root_url_resolves_to_home_page_view(self):
	# 	found = resolve('/')
	# 	self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		# request = httpRequest() # what Django will see when a user's browser asks for a page
		response = self.client.get('/') # passes the URL we want to test
		#response = home_page(request)

		# html = response.content.decode('utf8') # gets raw bytes then converts them to HTML
		# self.assertTrue(html.startswith('<html>'))
		# self.assertIn('<title>To-Do lists</title>', html)
		# self.assertTrue(html.endswith('</html>'))

		self.assertTemplateUsed(response, 'home.html') # checks which template (we want 'home.html') was used to render a response
	# def test_can_save_a_POST_request(self):
	# 	response = self.client.post('/', data={'item_text': 'A new list item'}) # to do a POST, we call self.client.post. Takes data argument
	# 	# containing the form data we want to send.

	# 	self.assertEqual(Item.objects.count(), 1)
	# 	new_item = Item.objects.first() # same asobjects.all()[0]
	# 	self.assertEqual(new_item.text, 'A new list item')

	# def test_redirects_after_POST(self):
	# 	response = self.client.post('/', data={'item_text': 'A new list item'}) # to do a POST, we call self.client.post. Takes data argument
	# 	self.assertEqual(response.status_code, 302) # We want to redirect the user back to the home page. the HTTP redirect has sc 302.
	# 	self.assertEqual(response['location'], '/lists/the-only-list-in-the-world')


	# def test_displays_all_list_items(self):
	# 	Item.objects.create(text="itemey 1")
	# 	Item.objects.create(text="itemey 2")

	# 	response = self.client.get('/')

	# 	self.assertIn('itemey 1', response.content.decode())
	# 	self.assertIn('itemey 2', response.content.decode())
		

class ListAndItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		save_items = Item.objects.all() # QuerySet which is a list-like
		self.assertEqual(save_items.count(), 2)

		first_saved_item = save_items[0]
		second_saved_item = save_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)

	# def test_only_saves_items_when_necessary(self):
	# 	self.client.get('/')
	# 	self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/') # the f string allows us to input a variable into the string
		self.assertTemplateUsed(response,'list.html')

	def test_displays_all_list_items(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'itemey 1') # assertContains better than assertIn
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1') # assertContains better than assertIn
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list) # response.context allows us to access a variable passed to the template

class NewListTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'}) # to do a POST, we call self.client.post. Takes data argument
		# containing the form data we want to send.
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first() # same as objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'}) # to do a POST, we call self.client.post. Takes data argument
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')
		# self.assertEqual(response.status_code, 302) # We want to redirect the user back to the home page. the HTTP redirect has sc 302.
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world')

class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
		    f'/lists/{correct_list.id}/add_item',
		    data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)


	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
		    f'/lists/{correct_list.id}/add_item',
		    data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')

