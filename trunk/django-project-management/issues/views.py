# Create your views here.
import simplejson as json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template.defaultfilters import slugify
from projects.models import *
from projects.views import updateLog
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success
from issues.forms import *
import time


@login_required
def add_issue(request, project_number):

	project = Project.objects.get(project_number=project_number)
	if request.method == 'POST':
		form = IssueForm(request.POST)
		if form.is_valid():
			t = form.save(commit=False)
			t.author = request.user
			t.save()
			project.issues.add(t)
			project.save()
			request.user.message_set.create(message='''Issue %s Registered''' % t.id)
			updateLog(request, project_number, '''Issue %s Registered''' % t.id)
			return HttpResponse( return_json_success() )
		else:
			return HttpResponse( handle_form_errors(form.errors))

@login_required
def edit_issue(request, project_number, issue_id):

	project = Project.objects.get(project_number=project_number)
	issue = Issue.objects.get(id=issue_id)
	if request.method == 'POST':
		form = IssueForm(request.POST, instance=issue)
		if form.is_valid():
			t = form.save()
			t.save()
			request.user.message_set.create(message='''Issue %s Edited''' % t.id)
			for change in form.changed_data:
				updateLog(request, project_number, 'Issue %s updated' % ( t.id ))
			return HttpResponse( return_json_success() )
		else:
			return HttpResponse( handle_form_errors(form.errors))

@login_required
def deleteIssue(request, projectNumber, issueSlug):

	project = Project.objects.get(projectNumber=projectNumber)
	issue = Issue.objects.get(slug=issueSlug)
	project.issues.remove(issue)
	request.user.message_set.create(message='''Issue %s Deleted''' % issue.slug)
	updateLog(request, projectNumber, '''Issue %s Deleted''' % issue.slug)
	return HttpResponseRedirect('/Projects/%s/Issues' % project.projectNumber)
	
			
	
@login_required
def view_issues(request, project_number):
	project = Project.objects.get(project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project

	return HttpResponse( serializers.serialize('json', project.issues.all(), relations=('owner', 'author'), display=['type', 'status', 'priority']))

@login_required
def view_issue(request, project_number, issue_id):
	issue = Issue.objects.get(id=issue_id)
	JSONSerializer = serializers.get_serializer('json')
	j = JSONSerializer()
	j.serialize([issue], fields=('description', 'owner', 'author', 'type', 'status', 'priority', 'related_rfc', 'related_helpdesk'))
	
	return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))
	