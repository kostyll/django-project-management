from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('rota.views',
	(r'MyRota/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/myrota.html' }),
	(r'MyRota/Ajax/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/ajax-myrota.html' }),
	(r'MyRota/$', 'view_rota', { 'year': False, 'month': False, 'day': False, 'template': 'rota/myrota.html' }),

	(r'TeamRota/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/teamrota.html'}),
	(r'TeamRota/Ajax/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/ajax-teamrota.html'}),
	(r'TeamRota/$', 'view_rota', { 'year': False, 'month': False, 'day': False, 'template': 'rota/teamrota.html' }),

	(r'AllRotas/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/allrota.html', 'pdf': False}),
	(r'AllRotas/Ajax/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/ajax-allrota.html', 'pdf': False}),
	(r'AllRotas/Ajax/EditForm/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/ajax_edit_rota.html', 'pdf': False}),
	(r'AllRotas/Ajax/Edit/(?P<username>[-\w\./\s]+)/(?P<shift>[-\w\./\s]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'edit_rota'),
	(r'AllRotas/Edit/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', 'view_rota', { 'template': 'rota/edit_rota.html', 'pdf': False}),
	(r'AllRotas/Edit/$', 'view_rota', { 'year': False, 'month': False, 'day': False, 'template': 'rota/edit_rota.html', 'pdf': False }),
	(r'AllRotas/Print/$', 'view_rota', { 'year': False, 'month': False, 'day': False, 'template': 'rota/rota-pdf.html', 'pdf': True }),
#	(r'AllRotas/$', 'view_rota', { 'year': False, 'month': False, 'day': False, 'template': 'rota/allrota.html', 'pdf': False, 'scope': 'all' }),
	(r'^All/$', 'rota_homepage'),
	(r'^RotaItems/$', 'view_rota_items'),

)

