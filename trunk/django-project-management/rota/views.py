# Create your views here.
import calendar
import datetime
import simplejson as json
import logging

from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from rota.models import RotaActivity, RotaItem, Team 
from wbs.models import EngineeringDay
from backends.pdfexport import render_to_pdf
import settings

@login_required
def view_users(request):
	return HttpResponse( serializers.serialize('json', User.objects.filter(is_active=True), fields=('id', 'username'), extras=('get_full_name')))

@login_required
def rota_homepage(request, rota_url):
	return render_to_response('rota/rota.html', {'rota_url': rota_url }, context_instance=RequestContext(request))
	
@login_required
def view_rota_activities(request):
	return HttpResponse( serializers.serialize('json', RotaActivity.objects.all()))	

@login_required
def view_rota(request, year=False, month=False, day=False, template=False, pdf=False, scope=False):
	
	# No additional security required here apart from a valid login. We allow all users to view 
	# their own rota plus the team and department rotas, and if they know the Edit Rota URL (hidden by default) they 
	# can load that page but not actually do anything in rota.views.edit_rota()

	cal = calendar.Calendar()
	now = datetime.datetime.now()										# now = datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
	today = datetime.date( now.year, now.month, now.day )

	if year and month and day:
		# User has asked for a specific week to be shown
		requested = datetime.date(int(year), int(month), int(day))	
	else:
		# Work out the days for this week
		requested = today
		
	this_week = calculate_week(requested)

	# [ { 'user': 'smorris', 'pk': '1', 'monday_rota': 'Infrastructure Mid', 'monday_eday': 'Free', 'tuesday_rota'
	ret = []

	logging.debug('''Requesting rota with scope => %s''' % ( scope ))

	if scope == 'all':
		scope_users = User.objects.filter(is_active=True).order_by('first_name').distinct()
	elif scope == 'team':
		scope_users = User.objects.filter(teams__in=request.user.teams.all(), is_active=True).order_by('first_name').distinct()
	else:
		scope_users = User.objects.filter(id=request.user.id)

	for u in scope_users:
		logging.debug('''Getting rota for %s''' % u)
		x = {'user': u.get_full_name(), 'pk': u.id }
		for day in this_week:
			try:
				_rota_item = RotaItem.objects.get(person=u, date=day)
				#logging.debug('''%s has %s as a rota item''' % ( u, _rota_item )
				rota_item = '''%s''' % _rota_item.activity
			
				logging.debug('''Found existing rota item for %s: %s''' % ( u, rota_item ))
			except RotaItem.DoesNotExist:
				rota_item = ''

			# Include engineering day information in the rota
			_engineering_days = EngineeringDay.objects.filter(work_date=day, resource=u)
			for e_day in _engineering_days:
				if e_day.wip_item.all():
					rota_item += '''%s<br>(%s) WIP Item''' % ( rota_item, e_day.get_day_type_display() )
				elif e_day.work_item.all():
					rota_item += '''%s<br>(%s) Project Work''' % ( rota_item, e_day.get_day_type_display() )
				else:
					pass
		
			x['''%s_r''' % day.isoweekday()] = str(rota_item)
				
		ret.append(x)

			
	return HttpResponse(json.dumps(ret))

@login_required
def edit_rota(request, year, month, day, shift, username):

	# Some security, if the user isn't allowed to edit the rota raise 404
	if not request.user.has_perm('rota.can_edit'):
		raise Http404
	
	date = datetime.date(int(year), int(month), int(day))	
	person = User.objects.get(username=username)
	activity = RotaActivity.objects.get(id=shift)

	try:
		r = RotaItem.objects.get(date=date, person=person)
	except RotaItem.DoesNotExist:
		r = RotaItem()	
			
	r.date=date	
	r.person=person
	r.activity=activity
	r.author=request.user
	r.save()
	return HttpResponse('Updated to %s' % r.activity )
	

def calculate_week(requested_date):

	''' Returns a list of days - this_week - given a date. '''

	cal = calendar.Calendar()
	day_of_week = calendar.weekday( requested_date.year, requested_date.month, requested_date.day ) 					# 0 = Monday, 1 = Tuesday, 2 = Wednesday
	monday_of_this_week = requested_date + datetime.timedelta(days=-day_of_week) 										# datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
	monday_of_this_week = datetime.date( monday_of_this_week.year, monday_of_this_week.month, monday_of_this_week.day )	# Abbreviate down to one day
	
	for week in cal.monthdatescalendar( requested_date.year, requested_date.month ):
		if monday_of_this_week in week:
			return week

