from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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