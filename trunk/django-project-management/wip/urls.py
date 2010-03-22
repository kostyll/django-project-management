from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('wip.views',
	(r'AjaxLoadForm/(?P<work_item_id>[-\w\./\s]+)/$', 'get_ajax_form'),
	(r'AddHeading/(?P<wip_report_id>[-\w\./\s]+)/$', 'add_heading'),
	(r'CloseHeading/(?P<heading_id>[-\w\./\s]+)/$', 'close_heading'),
	(r'AddWorkItem/(?P<heading_id>[-\w\./\s]+)/$', 'add_work_item'),
	(r'UpdateWorkItem/(?P<work_item_id>[-\w\./\s]+)/$', 'update_work_item'),
	(r'Ajax/EngineeringDay/(?P<work_item_id>[-\w\./\s]+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/(?P<day_type>\d{1})/$', 'get_resources_for_engineering_day'),
	(r'AddEngineeringDay/(?P<work_item_id>[-\w\./\s]+)/$', 'add_wip_engineering_day'),
	(r'Download/(?P<wip_report>[-\w\./\s]+)/$', 'download_wip_report'),
	(r'DownloadArchive/(?P<wip_archive>[-\w\./\s]+)/$', 'download_wip_archive'),
	(r'MyWIP/$', 'view_my_wip'),
	(r'(?P<wip_report>[-\w\./\s]+)/xhr/assignees/$', 'xhr_get_assignees'),
	(r'(?P<wip_report>[-\w\./\s]+)/$', 'view_wip_report'),
	(r'', 'all_wip_reports'),
)

