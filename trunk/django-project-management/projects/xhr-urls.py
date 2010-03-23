from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('projects.ext-views',
	(r'get_companies/$', 'get_companies'),
	(r'(?P<project_number>[-\w\./\s]+)/get_users/$', 'get_users'),
	(r'(?P<project_number>[-\w\./\s]+)/edit_pid$', 'edit_pid'),
)

