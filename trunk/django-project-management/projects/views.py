# Create your views here.
import datetime
import simplejson as json

from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from projects.models import *
from projects.forms import *
from risks.forms import RiskForm
from files.forms import FileForm
from issues.forms import IssueForm
from wip.models import WIPItem
from lessons.forms import LessonForm
from deliverables.forms import DeliverableForm
from backends.authlib import *
from backends.pdfexport import render_to_pdf
from rota.views import calculate_week
from projects.misc import check_project_read_acl, check_project_write_acl
from wbs.models import ProjectPhase

@login_required
def home_page(request):

	# Security - only show users projects that they are a member of a read ACL for
	projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
	wip_items = WIPItem.objects.filter(complete=False, assignee=request.user)

	# Get the rota items for this week
	now = datetime.datetime.now()										# now = datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
	today = datetime.date( now.year, now.month, now.day )
	this_week = calculate_week(today)
	return render_to_response('projects/home.html', {'projects': projects, 'wip_items': wip_items, 'this_week': this_week}, context_instance=RequestContext(request))


@login_required
def list_all_projects(request, pdf=False):
	
	projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
	if pdf:
		return render_to_pdf('files/project_status_pdf.html', {'projects': projects, 'title': 'Project Status', 'paper_orientation': 'landscape', 'paper_size': 'a3', 'files': settings.STATIC_DOC_ROOT }, filename="PROJECT_STATUS.pdf")
	else:
		return render_to_response('projects/list.html', {'projects': projects }, context_instance=RequestContext(request))

@login_required
def view_project(request, project_number):

	# Some security - only allow users to view objects they are allowed to via read_acl
	project = get_object_or_404(Project, project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project


	
	forms = {}
	forms['DialogEditCompany'] = DialogEditCompany(instance=project)
	forms['DialogEditProjectManager'] = DialogEditProjectManager(instance=project)
	forms['DialogEditTeamManagers'] = DialogEditTeamManagers(instance=project)
	forms['DialogEditProjectSponsor'] = DialogEditProjectSponsor(instance=project)
	forms['DialogEditProjectDescription'] = DialogEditProjectDescription(instance=project)
	forms['DialogEditBusinessCase'] = DialogEditBusinessCase(instance=project)
	forms['DialogEditBusinessBenefits'] = DialogEditBusinessBenefits(instance=project)
	forms['DialogEditProjectScope'] = DialogEditProjectScope(instance=project)
	forms['DialogEditExclusions'] = DialogEditExclusions(instance=project)
	forms['DialogEditAssumptions'] = DialogEditAssumptions(instance=project)
	forms['RiskForm'] = RiskForm()
	forms['DeliverableForm'] = DeliverableForm()
	forms['IssueForm'] = IssueForm(initial={'author': request.user.id})
	forms['LessonForm'] = LessonForm(initial={'author': request.user.id})
	forms['DialogUploadFile'] = FileForm(initial={'author': request.user.id})
	# There are 2 types of Executive Summary form, one for Project Managers... one for team members
	if request.user == project.project_manager:
		forms['ExecutiveSummary'] = DialogExecutiveSummary(initial={'author': request.user.id, 'type': 2})
	else:
		forms['ExecutiveSummary'] = DialogExecutiveSummary(initial={'author': request.user.id, 'type': 1})

	return render_to_response('projects/view-project.html', { 'project': project, 'forms': forms }, context_instance=RequestContext(request))

@login_required
def edit_project(request, project_number, form_type):

	# Some security - only allow users to view objects they are allowed to via write_acl
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to write to project

	if request.method == 'POST':
		form = eval(form_type)(request.POST, instance=project)
		if form.is_valid():
			t = form.save()
			for id in request.POST['team_managers_placeholder'].split(','):
				t.team_managers.add(id)
			t.save()
			request.user.message_set.create(message='''Project %s Edited''' % t.project_number)
			for change in form.changed_data:
				updateLog(request, t.project_number, '%s Updated' % change)
			ret = {"success": True}
			return HttpResponse(json.dumps(ret))
		else:
			print form.errors
			pass

@login_required
def updateLog(request, project_number, message):
	project = Project.objects.get(project_number=project_number)
	x = HistoryLog()
	x.project = project
	x.user = request.user
	x.description = message
	x.save()

@login_required
def viewHistory(request, projectNumber):

	project = Project.objects.get(projectNumber=projectNumber)
	history = HistoryLog.objects.filter(project=project)
	return render_to_response('projects/history.html', { 'project': project, 'history': history }, context_instance=RequestContext(request))
	
@login_required
def add_checkpoint_report(request, project_number):

	# Some security - only allow users to view objects they are allowed to via write_acl
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to write to project

	if request.method == 'POST':
		form = DialogExecutiveSummary(request.POST)
		if form.is_valid():
			t = form.save()
			project.executive_summary.add(t)
			project.save()
			request.user.message_set.create(message='''Checkpoint Report added''')
			return HttpResponseRedirect('''%s''' % project.get_absolute_url())
		else:
			pass

@login_required
def view_checkpoint_reports(request, project_number):	
	# Some security - only allow users to view objects they are allowed to via write_acl
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to write to project
	return HttpResponse( serializers.serialize('json', project.executive_summary.all(), relations=('author',), display=['type']))


@login_required
def view_project_phases(request, project_number):
	# Some security - only allow users to view objects they are allowed to via write_acl
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to write to project
	return HttpResponse( serializers.serialize('json', ProjectPhase.objects.filter(work_items__project=project)))
