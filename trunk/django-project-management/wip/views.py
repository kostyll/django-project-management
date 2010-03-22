# Create your views here.
import time
import datetime
import simplejson as json

from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.html import urlize

from wip.models import *
from wip.forms import WIPItemEditorForm, WIPItemUserForm, WIPHeadingForm
from backends.pdfexport import render_to_pdf, html_to_pdf
from projects.models import UserProfile
from projects.misc import get_wip_assignee_list
from rota.models import RotaItem
from wbs.forms import EngineeringDayForm
import settings


@login_required
def view_my_wip(request):

	headings = Heading.objects.filter(wip_items__assignee=request.user).exclude(wip_items__complete=True)
	return render_to_response('wip/mywip.html', {'headings': headings }, context_instance=RequestContext(request))
	

@login_required
def download_wip_report(request, wip_report):
	
	wip_report = WIPReport.objects.get(name=wip_report)
	headings = Heading.objects.filter(report=wip_report)
	objectives = WIPItem.objects.filter(heading__report=wip_report, complete=False, objective=True)
	return render_to_pdf('wip/wip-pdf.html', {'wip_report': wip_report, 'headings': headings, 'objectives': objectives, 'files': settings.STATIC_DOC_ROOT,
												'paper_size': 'a3', 'paper_orientation': 'landscape' }, filename="%s-%s.pdf" % ( time.strftime("%Y-%m-%d"), wip_report.name.replace(' ', '_') ))
		
@login_required
def download_wip_archive(request, wip_archive):

	wip_report = get_object_or_404(WIPArchive, id=wip_archive)
	filename = '''%s-%s.pdf''' % ( wip_report.created_date.strftime("%Y-%m-%d"), wip_report.wip_report.name.replace(' ', '_'))
	return html_to_pdf( wip_report.html, filename="%s-%s.pdf" % ( wip_report.created_date.strftime("%Y-%m-%d"), wip_report.wip_report.name.replace(' ', '_') ))

	

@login_required
def all_wip_reports(request):

	wip_reports = WIPReport.objects.filter(active=True, read_acl__in=request.user.groups.all()).distinct()
	return render_to_response('wip/all_wips.html', {'wip_reports': wip_reports }, context_instance=RequestContext(request))


@login_required
def view_wip_report(request, wip_report):
	
	xhr = request.GET.has_key('xhr')

	wip_report = WIPReport.objects.get(name=wip_report)
	headings = Heading.objects.filter(report=wip_report)
	objectives = WIPItem.objects.filter(heading__report=wip_report, complete=False, objective=True)
	if xhr:
		return HttpResponse( serializers.serialize('json', WIPItem.objects.filter(heading__report=wip_report, complete=False), display=['status'], relations=('assignee','heading')))
	else:
		return render_to_response('wip/wip.html', {'wip_report': wip_report, 'headings': headings, 'objectives': objectives }, context_instance=RequestContext(request))

@login_required
def get_ajax_form(request, work_item_id):
	
	work_item = WIPItem.objects.get(id=work_item_id)

	# Some security.. if the user isn't allowed to read the WIP report this belongs to
	# redirect them. Otherwise give them back the appropriate form
	f = WIPItemUserForm(instance=work_item) 		# Give them the editor form unless we find they are an editor
	allow_access = False
	for group in request.user.groups.all():
		if group in work_item.heading.all()[0].report.all()[0].read_acl.all():
			allow_access = True
		if group in work_item.heading.all()[0].report.all()[0].write_acl.all():
			f = WIPItemEditorForm(instance=work_item, wip_report=work_item.heading.all()[0].report.all()[0])
			
	if allow_access:
		return HttpResponse(f.as_table())
	else:
		return HttpResponse(work_item_id.heading.all()[0].report.all()[0].get_absolute_url())
	

@login_required
def add_heading(request, wip_report_id):
	
	wip_report = get_object_or_404(WIPReport, id=wip_report_id)
	
	# Some security	
	allow_access = False		 
	for group in request.user.groups.all():
		if group in wip_report.write_acl.all():
			allow_access = True
	
	if allow_access:
		if request.method == 'POST':
			form = WIPHeadingForm(request.POST)
			if form.is_valid():
				t = form.save()
				wip_report.headings.add(t)
				wip_report.save()
				_add_wip_to_archive(wip_report)
				return HttpResponseRedirect(t.get_absolute_url())

	else:
		raise Http404	

@login_required
def add_work_item(request, heading_id):
	heading = get_object_or_404(Heading, id=heading_id)

	# Some security
	allow_access = False
	for group in request.user.groups.all():
		if group in heading.report.all()[0].write_acl.all():
			allow_access = True
		
	if allow_access:
		if request.method == 'POST':
			form = WIPItemEditorForm(heading.report.all()[0], request.POST)
			if form.is_valid():
				t = form.save()
				heading.wip_items.add(t)
				heading.save()
				_add_wip_to_archive(heading.report.all()[0])
				return HttpResponseRedirect(t.get_absolute_url())
			else:
				print form.errors

	else:
		raise Http404	
		
@login_required
def update_work_item(request, work_item_id):
	work_item = get_object_or_404(WIPItem, id=work_item_id)

	# Some security
	allow_access = False
	wip_report = work_item.heading.all()[0].report.all()[0]
	for group in request.user.groups.all():
		if group in wip_report.read_acl.all():
			allow_access = True
			form = WIPItemUserForm(request.POST, instance=work_item)
		if group in wip_report.write_acl.all():
			allow_access = True
			form = WIPItemEditorForm(wip_report, request.POST, instance=work_item)
	
	if allow_access:
		if form.is_valid():
			t = form.save(commit=False)
			
			if request.POST['update'] != '':			
				if request.user.get_full_name() == '':
					update_name = request.user.username
				else:
					update_name = request.user.get_full_name()
				t.history = '''\n\n------Updated by %s on %s------\n\n%s\n\n%s''' % ( update_name, time.strftime("%Y-%m-%d %H:%M"), form.cleaned_data.get('update'), work_item.history )

			# To make the WIP report run a little smoother.. if we are closing a WIP item we'll keep it in the database but unlink it from it's heading
			if 'complete' in form.changed_data:
				heading = work_item.heading.all()[0]
				heading.wip_items.remove(work_item)
				heading.save()
				t.save()
				_add_wip_to_archive(heading.report.all()[0])
				return HttpResponseRedirect(heading.get_absolute_url())
			else:
				t.save()
				_add_wip_to_archive(work_item.heading.all()[0].report.all()[0])
				return HttpResponseRedirect(t.get_absolute_url())

def _add_wip_to_archive(wip_report):
	
	headings = Heading.objects.filter(report=wip_report)
	objectives = WIPItem.objects.filter(heading__report=wip_report, complete=False, objective=True)
	
	try:
		today = datetime.date.today()
		day, month, year = today.day, today.month, today.year
		print '''WIPArchive.objects.get(created_date__day=%s, created_date__month=%s, created_date__year=%s)''' % ( day, month, year )
		archive = WIPArchive.objects.get(created_date__day=day, created_date__month=month, created_date__year=year)
	except WIPArchive.DoesNotExist:
		archive = WIPArchive()
	archive.wip_report = wip_report
	archive.html = render_to_string('wip/wip-pdf.html', {'wip_report': wip_report, 'headings': headings, 'objectives': objectives })
	archive.save()
			
			
def get_resources_for_engineering_day(request, work_item_id, year, month, day, day_type):
	
	work_item = get_object_or_404(WIPItem, id=work_item_id)
	wip_report = work_item.heading.all()[0].report.all()[0]
	requested_date = datetime.date(int(year), int(month), int(day))

	
	ret = [ ]
	resources = [ ]
	for user in User.objects.filter(is_active=True).order_by('username'):
		for group in user.groups.all():
			if group in wip_report.read_acl.all():
				if user not in resources:
					resources.append(user)
	print resources
	for res in resources:
		# Get the resources name
		if res.get_full_name() != '':
			res_full_name = res.get_full_name()
		else:
			res_full_name = res.username

		print res_full_name

		res_activity = EngineeringDay.objects.filter(work_date=requested_date, resource=res)

		print '''activity for %s''' % res_full_name, res_activity
		if len(res_activity) == 0: # Resource isn't booked at all
			str = '''<option value="%s">%s - Available all day</option>''' % ( res.id, res_full_name )
		
		elif len(res_activity) >= 2: # User already has 2 bookings for this day
			str = '''<option value="%s" disabled>%s - Booked out all day</option>''' % ( res.id, res_full_name )
		else:
			for day in res_activity:
				if day.day_type == 0:
					str = '''<option value="%s">%s - Available PM only</option>''' % ( res.id, res_full_name )
				elif day.day_type == 1:
					str = '''<option value="%s">%s - Available AM only</option>''' % ( res.id, res_full_name )
				elif day.day_type == 2:
					str = '''<option value="%s" disabled>%s - Not available</option>''' % ( res.id, res_full_name )


		try:
			r = RotaItem.objects.get(person=res, date=requested_date)
			if r.activity.unavailable_for_projects:
				str = '''<option value="%s" disabled>%s - Not available</option>''' % ( res.id, res_full_name )
		except RotaItem.DoesNotExist:
			pass
				
		
		ret.append(str)
	return HttpResponse(ret)

def add_wip_engineering_day(request, work_item_id):

	work_item = get_object_or_404(WIPItem, id=work_item_id)
	wip_report = work_item.heading.all()[0].report.all()[0]

	if request.method == 'POST':
		form = EngineeringDayForm(request.POST)
		if form.is_valid():
			t = form.save(commit=False)	
			t.save()
			work_item.engineering_days.add(t)
			work_item.save()
			return HttpResponseRedirect(work_item.get_absolute_url())
		else:
			print form.errors
			print request.POST['work_date']
	
	
def close_heading(request, heading_id):

	heading = Heading.objects.get(id=heading_id)
	wip_report = heading.report.all()[0]
	
	# Keep the heading in the database but disassociate with the WIP report
	wip_report.headings.remove(heading)
	wip_report.save()
	_add_wip_to_archive(wip_report)
	return HttpResponseRedirect(wip_report.get_absolute_url())
	
	
@login_required
def xhr_get_assignees(request, wip_report):
	
	wip_report = WIPReport.objects.get(name=wip_report)
	return HttpResponse( serializers.serialize('json', User.objects.filter( groups__in=wip_report.read_acl.all()).distinct(), excludes=('is_active', 'is_superuser', 'is_staff', 'last_login', 'groups', 'user_permissions', 'password', 'email', 'date_joined') ))
