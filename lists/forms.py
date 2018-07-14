from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

# forms can process user input and validate it for error, render HTML input elements
# and error messages, and some can save data to the database.

class ItemForm(forms.models.ModelForm): # ModelForms can do all sorts of smart stuff. Link: https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/
	def save(self, for_list):
		self.instance.list = for_list # The .instance attribute on a form represents the database object that is being modified or created
		return super().save()

	class Meta: # In Meta we specify which model the form is for, and which fields we cant it to use
		model = Item
		fields = ('text',)
		widgets = {
		'text': forms.fields.TextInput(attrs={
			'placeholder': 'Enter a to-do item',
			'class': 'form-control input-lg',
			})
		}
		error_messages = {
			'text': {'required': EMPTY_ITEM_ERROR}
		}
	# item_text = forms.CharField(
	# 	widget=forms.fields.TextInput(attrs={
	# 		'placeholder': 'Enter a to-do item',
	# 		'class': 'form-control input-lg'
	# 	}),
	# )
class ExistingListItemForm(ItemForm):
	def __init__(self, for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list

	def validate_unique(self): # basically takes the validation error, adjusts its error message, and then passes it back into the form.
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)

	def save(self):
		return forms.models.ModelForm.save(self)