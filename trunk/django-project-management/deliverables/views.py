# Create your views here.
import simplejson as json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response
from django.db.models import Q
from projects.models import *
from projects.views import updateLog
from deliverables.forms import *

@login_required
def add_deliverable(request, project_number):

	project = Project.objects.get(project_number=project_number)
	if request.method == 'POST':
		form = DeliverableForm(request.POST)
		if form.is_valid():
			t = form.save()
			t.save()
			project.deliverables.add(t)
			project.save()
			request.user.message_set.create(message='''Deliverable %s Registered''' % t.id)
			updateLog(request, project_number, '''Deliverable %s Registered''' % t.id)
			ret = {"success": True}
			return HttpResponse(json.dumps(ret))
		else:
			pass

@login_required
def edit_deliverable(request, project_number, deliverable_id):

	project = Project.objects.get(project_number=project_number)
	deliverable = Deliverable.objects.get(id=deliverable_id)
	if request.method == 'POST':
		form = DeliverableForm(request.POST, instance=deliverable)
		if form.is_valid():
			t = form.save()
			t.save()
			request.user.message_set.create(message='''Deliverable %s Edited''' % t.id)
			for change in form.changed_data:
				updateLog(request, project_number, '''%s changed to %s''' % ( change, eval('''t.%s''' % change)))		
			ret = {"success": True}
			return HttpResponse(json.dumps(ret))
		else:
			pass

@login_required
def deleteDeliverable(request, projectNumber, deliverableSlug):

	project = Project.objects.get(projectNumber=projectNumber)
	deliverable = Deliverable.objects.get(slug=deliverableSlug)
	project.deliverables.remove(deliverable)
	request.user.message_set.create(message='''Deliverable %s Deleted''' % deliverable.slug )
	updateLog(request, projectNumber, '''Deliverable %s Deleted''' % deliverable.slug)
	return HttpResponseRedirect('/Projects/%s/Deliverables' % project.projectNumber)
	
@login_required
def view_deliverables(request, project_number):
	project = Project.objects.get(project_number=project_number)
	return HttpResponse( serializers.serialize('json', project.deliverables.all()))
	
@login_required
def view_deliverable(request, project_number, deliverable_id):
	deliverable = Deliverable.objects.get(id=deliverable_id)
	JSONSerializer = serializers.get_serializer('json')
	j = JSONSerializer()
	j.serialize([deliverable], fields=('description', 'acceptance_criteria', 'deliverable_tester', 'testing_method', 'expected_result', 'rpo', 'rto'))
	
	return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))



