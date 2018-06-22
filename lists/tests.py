from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

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
	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_text': 'A new list item'}) # to do a POST, we call self.client.post. Takes data argument
		# containing the form data we want to send.
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')

class ItemNodelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		save_items = Item.objects.all() # QuerySet which is a list-like
		self.assertEqual(save_items.count(), 2)

		first_saved_item = save_items[0]
		second_saved_item = save_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')
		