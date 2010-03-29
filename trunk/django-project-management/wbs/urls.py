from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('wbs.views',
	(r'(?P<project_number>[-\w\./\s]+)/StagePlan/Add/$', 'add_project_stage'),
	(r'(?P<project_number>[-\w\./\s]+)/StagePlan/$', 'view_stage_plan'),
	(r'(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)/Edit/$', 'edit_work_item'),
	(r'(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)/Delete/$', 'delete_work_item'),
	(r'(?P<project_number>[-\w\./\s]+)/Edit/$', 'edit_wbs'),
	(r'(?P<project_number>[-\w\./\s]+)/Add/$', 'add_work_item'),
	(r'(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)/AddEngineeringDay/$', 'add_engineering_day'),
	(r'(?P<project_number>[-\w\./\s]+)/WBSReorder/$', 'reorder_wbs'),
	(r'(?P<project_number>[-\w\./\s]+)/Ajax/EngineeringDay/(?P<wbs_id>[-\w\./\s]+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/(?P<day_type>\d{1})/$', 'get_resources_for_engineering_day'),
	(r'(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)$', 'view_work_item'),
	(r'(?P<project_number>[-\w\./\s]+)/$', 'view_wbs'),
)

