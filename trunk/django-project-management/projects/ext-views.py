import simplejson as json

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core import serializers
from projects.models import *
from projects.misc import check_project_read_acl, check_project_write_acl

@login_required
def get_companies(request):
	return HttpResponse( serializers.serialize('json', Company.objects.filter(active=True)))	

@login_required
def get_users(request, project_number):
	project = get_object_or_404(Project, project_number=project_number)
	return HttpResponse( serializers.serialize('json', User.objects.filter( groups__in=project.read_acl.all()).distinct(), excludes=('is_active', 'is_superuser', 'is_staff', 'last_login', 'groups', 'user_permissions', 'password', 'email', 'date_joined') ))
	
@login_required
def edit_pid(request, project_number):
	# Some security - only allow users to view objects they are allowed to via read_acl
	project = get_object_or_404(Project, project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project

	JSONSerializer = serializers.get_serializer('json')
	j = JSONSerializer()
	j.serialize([project], fields=('project_name', 'project_number', 'project_status', 'company', 'project_manager', 'team_managers', 'project_sponsor', 'project_description', 'business_case', 'business_benefits', 'project_scope', 'exclusions', 'assumptions'))
	return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))
	
