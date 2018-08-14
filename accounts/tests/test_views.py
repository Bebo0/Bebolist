# mocks are a useful tool for unit testing external dependencies, 
# example: sending an email. Any interaction with a third-party API is a
# good candidate for testing with mocks.

from django.test import TestCase
from unittest.mock import patch # Python has a built in library for mocking
import accounts.views

class SendLoginEmailViewTest(TestCase):

	def test_redirect_to_home_page(self):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
			})
		self.assertRedirects(response, '/')

	@patch('accounts.views.send_mail') # Replaces target function (i.e send_mail) with a mock for the duration of the function
	def test_sends_mail_to_address_from_post(self, mock_send_mail): # Patch then injects target function into test function
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com' # We call our function normally. The view won't call send_mail, but mock_send_mail instead
			})

		# def fake_send_mail(subject, body, from_email, to_list): # We define a mock function
		# 	# All it does is save some info about how the fxn was called. Called monkeypatching
		# 	self.send_mail_called = True
		# 	self.subject = subject
		# 	self.body = body
		# 	self.from_email = from_email
		# 	self.to_list = to_list

		# accounts.views.send_mail = fake_send_mail # Before code is executed, we swap the real fxn with the mock one

		# self.client.post('/accounts/send_login_email', data={
		# 	'email': 'edith@example.com'
		# })

		self.assertTrue(mock_send_mail.called)
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args # We can unpack the arguments that a fxn was called using
		self.assertEqual(subject, 'Your login link for Bebolist')
		self.assertEqual(from_email, 'noreply@bebolist')
		self.assertEqual(to_list, ['edith@example.com'])