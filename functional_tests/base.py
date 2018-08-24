from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from unittest import skip
from .server_tools import reset_database

# from django.test import LiveServerTestCase # need to switch to StaticLiveServerTestCase when we add static files
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time
import unittest

import os

MAX_WAIT = 10

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
				time.sleep(2)
	return modified_fn


# class NewVisitorTest(LiveServerTestCase):
class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.staging_server = os.environ.get('STAGING_SERVER') # using an environment variable called STAGING_SERVER
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server # We change the test server in LiveServerTestCase to point to our real server
			reset_database(self.staging_server) # Will reset the database between each test

	def tearDown(self):
		self.browser.quit()

	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])


	@wait
	def wait_for(self, fn):
		return fn()


	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)

	def add_list_item(self, item_text):
		num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
		self.get_item_input_box().send_keys(item_text)
		self.get_item_input_box().send_keys(Keys.ENTER)
		item_number = num_rows + 1
		self.wait_for_row_in_list_table(f'{item_number}: {item_text}')
