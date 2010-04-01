from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('rota.views',
	(r'RotaItems/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'view_rota', { 'template': 'rota/ajax-allrota.html', 'pdf': False}),
	(r'^All/$', 'rota_homepage'),
	(r'^RotaActivities/$', 'view_rota_activities'),
	(r'^RotaItems/$', 'view_rota'),
	(r'^Rota/$', 'view_rota_items'),
	(r'^Users/$', 'view_users'),

)

