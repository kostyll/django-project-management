from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('projects.views',
	(r'StatusReport/$', 'list_all_projects', { 'pdf': True }),
	(r'(?P<project_number>[-\w\./\s]+)/Edit/AddCheckPointReport/$', 'add_checkpoint_report'),
	(r'(?P<project_number>[-\w\./\s]+)/Edit/(?P<form_type>[-\w\./\s]+)/$', 'edit_project'),
	(r'(?P<project_number>[-\w\./\s]+)/Updates/$', 'view_checkpoint_reports'),
	(r'(?P<project_number>[-\w\./\s]+)/$', 'view_project'),
    (r'^$', 'list_all_projects'),
)

