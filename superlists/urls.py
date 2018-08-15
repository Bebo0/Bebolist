"""superlists URL Configuration

## This file is meants for URLs that apply to the entire site.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from lists import views as list_views
from lists import urls as list_urls
from accounts import urls as accounts_urls

# r'^$ is just the empty string aka '/' aka the root page
urlpatterns = [
    url(r'^$', list_views.home_page, name = 'home'),
    url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(accounts_urls))
    # url(r'^lists/new$', views.new_list, name='new_list'),
    # url(r'^lists/(\d+)/$', views.view_list, name='view_list'), # the (.+) will match any characters up to the following /
    # # Also, now we are passing an argument to the view function view_list()
    # url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),
]
