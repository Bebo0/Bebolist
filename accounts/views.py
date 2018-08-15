from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import Token
from django.core.urlresolvers import reverse


def send_login_email(request):
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri( # allows us to build a full URL 
		reverse('login') + '?token=' + str(token.uid)
		)
	message_body = f'Use this link to log in: \n\n{url}'
	send_mail(
		'Your login link for Bebolist',
		message_body,
		'noreply@bebolist',
		[email]
		)
	messages.success(request, # The green highlighted message on the page
		"Check your email, we've sent you a link you can use to log in.")
	return redirect('/')

def login(request):
	return redirect('/')