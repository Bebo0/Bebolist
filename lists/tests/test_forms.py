from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)

from lists.models import Item, List




class ItemFormTest(TestCase):

	def test_form_renders_item_text_input(self):
		form = ItemForm(data={'text': ''})
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())
		# self.fail(form.as_p()) # form.as_p() renders the form as HTML.

	def test_form_validation_for_blank_items(self):
		form = ItemForm(data={'text': ''})
		# form.save() # this will give an error b/c can't pass an empty string
		self.assertFalse(form.is_valid()) # populates the form's errors attribute
		self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

	def test_form_save_handles_saving_to_a_list(self):
		list_ = List.objects.create()
		form = ItemForm(data={'text': 'do me'})
		new_item = form.save(for_list=list_)
		self.assertEqual(new_item, Item.objects.first())
		self.assertEqual(new_item.text, 'do me')
		self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):

	def test_form_renders_item_text_input(self):
		form = ItemForm(data={'text': ''})
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())
		# self.fail(form.as_p()) # form.as_p() renders the form as HTML.

	def test_form_validation_for_blank_items(self):
		form = ItemForm(data={'text': ''})
		# form.save() # this will give an error b/c can't pass an empty string
		self.assertFalse(form.is_valid()) # populates the form's errors attribute
		self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

	def test_form_validation_for_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='no twins!')
		form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])