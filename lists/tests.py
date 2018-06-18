from django.test import TestCase

# functional test from users's persepctive
# unittest from programmer's perspective
# TestCase is an augmented version of unittest.TestCase
# run file using python manage.py test

class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1 + 1, 3)
		
