# Create your views here.
import datetime
import time

from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

from projects.models import *
from wbs.models import *
from wbs.forms import *
from rota.models import RotaItem
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

@login_required
def edit_wbs(request, project_number):

	project = get_object_or_404(Project, project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project

	forms = {}
	forms['WBSReorderForm'] = WBSReorderForm()
	forms['WBSForm'] = WBSForm(project)

	if request.method == 'POST':
		pass

	else:
		return render_to_response('wbs/edit_wbs.html', {'project': project, 'forms': forms}, context_instance=RequestContext(request))

@login_required
def add_project_stage(request, project_number):

	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	
	if request.method == 'POST':
		form = WBSProjectStage(request.POST)
		if form.is_valid():
			t = form.save()
			project.stage_plan.add(t)
			project.save()
			return HttpResponse( return_json_success() )
		else:
			return HttpResponse( handle_form_errors(form.errors))

@login_required
def view_stage_plan(request, project_number):

	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	return HttpResponse( serializers.serialize('json', project.stage_plan.all()))
			
	

@login_required
def reorder_wbs(request, project_number):
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	new_order = request.POST['work_item_order']

	new_order_list = [ ]
	for id in new_order.split('id[]='):
		id = id.replace('&','')
		new_order_list.append(id)

	i = 1
	for id in new_order_list:
		if id != '':
			wbs = WorkItem.objects.get(id=id)
			wbs.wbs_number = i
			wbs.save()
			i += 1
	return HttpResponseRedirect('''/WBS/%s/Edit/''' % project.project_number)

@login_required
def add_work_item(request, project_number):
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	if request.method == 'POST':
		form = WBSForm(project, request.POST)
		if form.is_valid():
			t = form.save(commit=False)
			number_of_items = WorkItem.objects.filter(active=True, project__id=project.id).count()
			t.wbs_number = number_of_items + 1	
			t.author = request.user
			t.save()
			project.work_items.add(t)
			project.save()
			return HttpResponse( return_json_success() )
		else:
			return HttpResponse( handle_form_errors(form.errors))
	
@login_required
def delete_work_item(request, project_number, wbs_id):
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	work_item = WorkItem.objects.get(id=wbs_id)

	project.work_items.remove(work_item)
	project.save()
	return HttpResponse( return_json_success() )

@login_required
def edit_work_item(request, project_number, wbs_id):
	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	work_item = WorkItem.objects.get(id=wbs_id)

	# Give the user the correct form - WBSForm for a project admin (has write access to project) or WBSUserForm for a readonly user
	form_type = 'WBSUserForm'
	for group in request.user.groups.all():
		if group in project.write_acl.all():
			form_type = 'WBSForm'

	if request.method == 'POST':
		form = eval(form_type)(project, request.POST, instance=work_item)
		if form.is_valid():
			t = form.save(commit=False)
			t.author = request.user

			if request.POST['update'] != '':			
				if request.user.get_full_name() == '':
					update_name = request.user.username
				else:
					update_name = request.user.get_full_name()
				t.history = '''\n\n------Updated by %s on %s------\n\n%s\n\n%s''' % ( update_name, time.strftime("%Y-%m-%d %H:%M"), form.cleaned_data.get('update'), work_item.history )



			t.save()
			return HttpResponseRedirect('''/WBS/%s/Edit/''' % project.project_number)
		else:
			print form.errors

	else:
		form = eval(form_type)(project, instance=work_item)
		return render_to_response('wbs/edit_work_item.html', {'project': project, 'work_item': work_item, 'form': form, 'action': '''/WBS/%s/%s/Edit/''' % ( project.project_number, work_item.id ) }, context_instance=RequestContext(request))
			
			
@login_required
def get_resources_for_engineering_day(request, project_number, wbs_id, year, month, day, day_type):


	project = get_object_or_404(Project, project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project

	work_item = WorkItem.objects.get(id=wbs_id)
	requested_date = datetime.date(int(year), int(month), int(day))
	
	ret = [ ]
	
	resources = UserProfile.objects.filter(skillset=work_item.skill_set, user__is_active=True)
	for res in resources:
		# Get the resources name
		if res.user.get_full_name() != '':
			res_full_name = res.user.get_full_name()
		else:
			res_full_name = res.user.username


		res_activity = EngineeringDay.objects.filter(work_date=requested_date, resource=res.user)

		if len(res_activity) == 0: # Resource isn't booked at all
			str = '''<option value="%s">%s - Available all day</option>''' % ( res.user.id, res_full_name )
		
		elif len(res_activity) >= 2: # User already has 2 bookings for this day
			str = '''<option value="%s" disabled>%s - Booked out all day</option>''' % ( res.user.id, res_full_name )
		else:
			for day in res_activity:
				if day.day_type == 0:
					str = '''<option value="%s">%s - Available PM only</option>''' % ( res.user.id, res_full_name )
				elif day.day_type == 1:
					str = '''<option value="%s">%s - Available AM only</option>''' % ( res.user.id, res_full_name )
				elif day.day_type == 2:
					str = '''<option value="%s" disabled>%s - Not available</option>''' % ( res.user.id, res_full_name )


		try:
			r = RotaItem.objects.get(person=res.user, date=requested_date)
			if r.activity.unavailable_for_projects:
				str = '''<option value="%s" disabled>%s - %s</option>''' % ( res.user.id, res_full_name, r.activity )
		except RotaItem.DoesNotExist:
			pass
				
		
		ret.append(str)
				
		
		
	ret.sort()
	return HttpResponse(ret)

@login_required
def add_engineering_day(request, project_number, wbs_id):

	project = get_object_or_404(Project, project_number=project_number)
	check_project_write_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	work_item = WorkItem.objects.get(id=wbs_id)
		
	if request.method == 'POST':
		form = EngineeringDayForm(request.POST)
		if form.is_valid():
			t = form.save(commit=False)	
			t.save()
			work_item.engineering_days.add(t)
			work_item.save()
			return HttpResponseRedirect('''/WBS/%s/Edit/''' % project.project_number)
		else:
			print form.errors
			print request.POST['work_date']
	
@login_required
def view_wbs(request, project_number):
	project = get_object_or_404(Project, project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project
	
	return HttpResponse( serializers.serialize('json', project.work_items.all(), relations=('skill_set','project_stage','author','owner'), extras=('get_work_item_status',)))
	
@login_required
def view_work_item(request, project_number, wbs_id):
	return HttpResponse( serializers.serialize('json', WorkItem.objects.filter(id=wbs_id), relations=('author', 'owner')))	
