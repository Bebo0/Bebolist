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

	@skip
	def test_cannot_add_empty_list_items(self):
	    # Edith goes to the home page and accidentally tries to submit
	    # an empty list item. She hits Enter on the empty input box

	    # The home page refreshes, and there is an error message saying
	    # that list items cannot be blank

	    # She tries again with some text for the item, which now works

	    # Perversely, she now decides to submit a second blank list item

	    # She receives a similar warning on the list page

	    # And she can correct it by filling some text in
	    self.fail('write me!')