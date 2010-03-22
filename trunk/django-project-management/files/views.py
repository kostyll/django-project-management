# Create your views here.
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from projects.models import *
from deliverables.models import *
from risks.models import *
from files.forms import *
from backends.pdfexport import render_to_pdf
import settings


@login_required
def project_pid(request, project_number):

	project = Project.objects.get(project_number=project_number)
	return render_to_pdf('files/pid.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number }, filename="%s_PROJECT_INITIATION_DOCUMENT.pdf" % project.project_number )

@login_required
def risk_register(request, project_number):

	project = Project.objects.get(project_number=project_number)
	return render_to_pdf('files/risk_register.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'landscape' }, filename="%s_RISK_REGISTER.pdf" % project.project_number )


@login_required
def gantt_chart(request, project_number):

	project = Project.objects.get(project_number=project_number)
	#return render_to_pdf('files/gantt.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_size': 'a3', 'paper_orientation': 'landscape' }, filename="%s_GANTT_CHART.pdf" % project.project_number )
	return render_to_response('files/gantt.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_size': 'a3', 'paper_orientation': 'landscape' }, context_instance=RequestContext(request))

@login_required
def work_breakdown_structure(request, project_number):

	project = Project.objects.get(project_number=project_number)
	return render_to_pdf('files/wbs.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'landscape', 'paper_size': 'a3' }, filename="%s_WORK_BREAKDOWN_STRUCTURE.pdf" % project.project_number )
#	return render_to_response('files/wbs.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'portrait' }, context_instance=RequestContext(request) )


@login_required
def issue_log(request, project_number):

	project = Project.objects.get(project_number=project_number)
	return render_to_pdf('files/issue.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'landscape', 'paper_size': 'a4' }, filename="%s_ISSUE_LOG.pdf" % project.project_number )
#	return render_to_response('files/wbs.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'portrait' }, context_instance=RequestContext(request) )

@login_required
def add_file(request, project_number):
	
	project = Project.objects.get(project_number=project_number)
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			t = form.save()
			project.files.add(t)
			project.save()
			return HttpResponseRedirect('''%s''' % project.get_absolute_url())
		
		else:
			print form.errors
			pass	
