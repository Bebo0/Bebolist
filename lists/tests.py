from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

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

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest() # what Django will see when a user's browser asks for a page
		response = home_page(request)
		html = response.content.decode('utf8') # gets raw bytes then converts them to HTML
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>', html)
		self.assertTrue(html.endswith('</html>'))
