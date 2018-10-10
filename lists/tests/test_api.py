# REST API:
# Our new URL structure will be /api/lists/{id}
# GET will give you details of a list (including all its items) in JSON format
# POST lets you add an item

import json
from django.test import TestCase

from lists.models import List, Item

class ListAPITest(TestCase):
	base_url = '/api/lists/{}/'

	def test_get_returns_json_200(self):
		list_ = List.objects.create()
		response = self.client.get(self.base_url.format(list_.id))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 
			'application/json')	

	def test_get_returns_items_for_correct_list(self):
			other_list = List.objects.create()
			Item.objects.create(list=other_list, text='item 1')
			our_list = List.objects.create()
			item1 = Item.objects.create(list=our_list, text='item 1')	
			item2 = Item.objects.create(list=our_list, text='item 2')	
			response = self.client.get(self.base_url.format(our_list.id))
			self.assertEqual(
				json.loads(response.content.decode('utf8')), # we expect
				# the response to be in json format. We use json.loads()
				# b/c it's easier to test Python objects than messing with raw JSON strings
				[
					{'id': item1.id, 'text': item1.text},
					{'id': item2.id, 'text': item2.text},

				]
			)

	def test_POSTing_a_new_item(self):
		list_ = List.objects.create()
		response = self.client.post(
			self.base_url.format(list_.id), 
			{'text': 'new item'},
		)
		self.assertEqual(response.status_code, 201)
		new_item = list_.item_set.get()
		self.assertEqual(new_item.text, 'new item')