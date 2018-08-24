from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from lists.views import home_page
from lists.models import Item, List

User = get_user_model()
# functional test from users's persepctive
# unittest from programmer's perspective
# TestCase is an augmented version of unittest.TestCase
# run file using python manage.py test

# Django's main job is to decide what to do whe a user asks for a particular
# URL on our site. Django's workflow is like this:
#
# 1) An HTTP request comes in for a particular URL
# 2) Django uses some ruleps to decide which view function should deal with the
# request (referred to as resolving the URL)
# 3) The view function processes the request and returns an HTTP response

class ListModelTest(TestCase):
	def test_get_absolute(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

	def test_lists_can_have_owners(self):
		user = User.objects.create(email='a@b.com')
		list_ = List.objects.create(owner=user)
		self.assertIn(list_, user.list_set.all())

	def test_list_owner_is_optional(self):
		List.objects.create() # Should not raise


class ItemModelTest(TestCase):

	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())

	# def test_saving_and_retrieving_items(self):
	# 	list_ = List()
	# 	list_.save()
		
	# 	first_item = Item()
	# 	first_item.text = 'The first (ever) list item'
	# 	first_item.list = list_
	# 	first_item.save()

	# 	second_item = Item()
	# 	second_item.text = 'Item the second'
	# 	second_item.list = list_
	# 	second_item.save()

	# 	saved_list = List.objects.first()
	# 	self.assertEqual(saved_list, list_)

	# 	save_items = Item.objects.all() # QuerySet which is a list-like
	# 	self.assertEqual(save_items.count(), 2)

	# 	first_saved_item = save_items[0]
	# 	second_saved_item = save_items[1]
	# 	self.assertEqual(first_saved_item.text, 'The first (ever) list item')
	# 	self.assertEqual(first_saved_item.list, list_)
	# 	self.assertEqual(second_saved_item.text, 'Item the second')
	# 	self.assertEqual(second_saved_item.list, list_)

	def test_cannot_save_empty_list_items(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError): # the 'with' wraps a block of code with some kind of setup, cleanup, or error-handling code.
			item.save()
			item.full_clean() # runs full database validation

		# alternatively, we could've written:
		# try:
		# 	item.save()
		# 	self.fail('The save should have raised an exception')
		# except ValidationError:
		# 	pass

	

	def test_duplicate_items_are_invalid(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='bla')
		with self.assertRaises(ValidationError):
			item = Item(list=list_, text='bla')
			item.full_clean()

	def test_CAN_save_same_item_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='bla')
		item = Item(list=list2, text='bla')
		item.full_clean()  # should not raise


	# def test_only_saves_items_when_necessary(self):
	# 	self.client.get('/')
	# 	self.assertEqual(Item.objects.count(), 0)

