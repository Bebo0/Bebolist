from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

# forms can process user input and validate it for error, render HTML input elements
# and error messages, and some can save data to the database.

class ItemForm(forms.models.ModelForm): # ModelForms can do all sorts of smart stuff. Link: https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/

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