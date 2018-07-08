from .base import FunctionalTest
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


class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		## We'll use a CSS class called .has-error to mark our error text
		## lambda example: myfn = lambda x: x + 1
		## myfn(2) = 3
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text, 
			"You can't have an empty list item!"))  

		# She tries again with some text for the item, which now works
		self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Perversely, she now decides to submit a second blank list item
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# She receives a similar warning on the list page
		self.wait_for(lambda: self.assertEqual(
		    self.browser.find_element_by_css_selector('.has-error').text,
		    "You can't have an empty list item"
		))

		# And she can correct it by filling some text in
		self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')