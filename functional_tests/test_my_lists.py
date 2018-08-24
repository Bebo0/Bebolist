from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

""" Each client (IP) is given a unique session ID which is stored in a cookie and submitted with ever request.
The server will store this ID somewhere (typically in the database) and then it
can recognize each request that comes in as being from a particular client.
The server can mark a client's session as being an authenticated (logged in) session
and associate it with a user ID in its database. 

A session is a dictionary-like data structure, and the user ID is stored under the key 
given by django.contrib.auth.SESSION_KEY.
"""

class MyListsTest(FunctionalTest):

	def create_pre_authenticated_session(self, email):
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
			print('\n\n\n\n')
			print(session_key)
			# session_key = create_session_on_server(self.staging_server, email)
		else:
			session_key = create_pre_authenticated_session(email)
			
		# user = User.objects.create(email=email)
		# session = SessionStore()
		# session[SESSION_KEY] = user.pk # we create a session object in the db
		# # the session key is the primary key of the user object which is actually the user's email address
		# session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		# session.save()
		## to set a cookie we need to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key, # we then add a cookie to the browser that matches the session on the server.
			# on our next visit to the site, the server should recognize us as a logged-in user.
			path='/',
		))
		# time.sleep(2)

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		# Edith is a logged-in user
		self.create_pre_authenticated_session('edith@example.com')

		# She goes to the home page and starts a list
		self.browser.get(self.live_server_url)
		self.add_list_item('Reticulate splines')
		self.add_list_item('Immanentize eschaton')
		first_list_url = self.browser.current_url

		# She notices a "My lists" link, for the first time.
		self.browser.find_element_by_link_text('My lists').click()

		# She sees that her list is in there, named according to its
		# first list item
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Reticulate splines')
			)
		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
			)
		 # She decides to start another list, just to see
		self.browser.get(self.live_server_url)
		self.add_list_item('Click cows')
		second_list_url = self.browser.current_url

		# Under "my lists", her new list appears
		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Click cows')
			)

		# She logs out.  The "My lists" option disappears
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(
			lambda: self.assertEqual(
				self.browser.find_element_by_link_text('My lists'),
				[]
			))


# Locally:
# +-----------------------------------+       +-------------------------------------+
# | MyListsTest                       |  -->  | .management.commands.create_session |
# | .create_pre_authenticated_session |       |  .create_pre_authenticated_session  |
# |            (locally)              |       |             (locally)               |
# +-----------------------------------+       +-------------------------------------+
# Against staging:
# +-----------------------------------+       +-------------------------------------+
# | MyListsTest                       |       | .management.commands.create_session |
# | .create_pre_authenticated_session |       |  .create_pre_authenticated_session  |
# |            (locally)              |       |            (on server)              |
# +-----------------------------------+       +-------------------------------------+
#             |                                                   ^
#             v                                                   |
# +----------------------------+     +--------+      +------------------------------+
# | server_tools               | --> | fabric | -->  | ./manage.py create_session   |
# | .create_session_on_server  |     |  "run" |      |   (on server, using .env)    |
# |        (locally)           |     +--------+      +------------------------------+

