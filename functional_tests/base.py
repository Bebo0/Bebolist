from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from unittest import skip

# from django.test import LiveServerTestCase # need to switch to StaticLiveServerTestCase when we add static files
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time
import unittest

import os

MAX_WAIT = 10

# class NewVisitorTest(LiveServerTestCase):
class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER') # using an environment variable called STAGING_SERVER
		if staging_server:
			self.live_server_url = 'http://' + staging_server # We change the test server in LiveServerTestCase to point to our real server

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:

					raise e
				time.sleep(0.5)

	@wait
	def wait_for(self, fn):
		return fn()

	"""Our own wait decorator function
	
	A decorator is a way of modifying a function; it takes an function as an argument
	and returns another function as the modified or decorated version
	"""
	def wait(fn):
		def modified_fn(*args, **kwargs): # We specify that modified_fn may take any
		# arbitrary positional and keyword arguments
			start_time = time.time()
			while True:
				try:
					return fn(*args, **kwargs) # We pass those same arguments to fn when we call it
				except (AssertionError, WebDriverException) as e:
					if time.time() - start_time > MAX_WAIT:
						raise e
					time.sleep(0.5)
		return modified_fn

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name('email')

