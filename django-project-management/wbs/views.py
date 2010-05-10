# Create your views here.
import datetime
import time
import simplejson as json
import logging

from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
from projects.templatetags.project_tags import get_task_rag_status

@login_required
def edit_wbs(request, project_number):

        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project

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
        check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
        
        if request.method == 'POST':
                form = WBSProjectStage(request.POST)
                if form.is_valid():
                        t = form.save(commit=False)
                        t.stage = '''%s - %s''' % ( t.stage_number, t.stage )
                        t.save()
                        project.stage_plan.add(t)
                        project.save()
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

@login_required
def view_stage_plan(request, project_number):

        project = get_object_or_404(Project, project_number=project_number)
        check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
        return HttpResponse( serializers.serialize('json', project.stage_plan.all()))
                        
        

@login_required
def reorder_wbs(request, project_number):
    project = get_object_or_404(Project, project_number=project_number)
    check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
    new_order = request.POST['work_item_order']

    logging.debug('''New order = %s''' % new_order )
    new_order_list = [ ]
    for id in new_order.split(','):
        new_order_list.append(id)

    i = 1
    for id in new_order_list:
        if id != '':
            wbs = WorkItem.objects.get(id=id)
            wbs.wbs_number = i
            wbs.save()
            i += 1
    return HttpResponse( return_json_success())

@login_required
def add_work_item(request, project_number):
        project = get_object_or_404(Project, project_number=project_number)
        check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
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
        check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
        work_item = WorkItem.objects.get(id=wbs_id)

        project.work_items.remove(work_item)
        project.save()
        return HttpResponse( return_json_success() )

@login_required
def edit_work_item(request, project_number, wbs_id):
        project = get_object_or_404(Project, project_number=project_number)
        check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
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
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

                        
                        
@login_required
def get_resources_for_engineering_day(request, project_number, wbs_id, year, month, day, day_type, as_json=True):


        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project

        work_item = WorkItem.objects.get(id=wbs_id)
        requested_date = datetime.date(int(year), int(month), int(day))
        
        ret = [ ]
        
        resources = UserProfile.objects.filter(skillset=work_item.skill_set, user__is_active=True).order_by('user__first_name')
        logging.debug('''Potential resources: %s.''' % resources)
        for res in resources:
                # Get the resources name
                if res.user.get_full_name() != '':
                        res_full_name = res.user.get_full_name()
                else:
                        res_full_name = res.user.username

                logging.debug('''Searching for Engineering days: work_date=%s, resource=%s, resource_id=%s''' % ( requested_date, res_full_name, res.user.id ))
                

                res_activity = EngineeringDay.objects.filter(work_date=requested_date, resource=res.user)

                r = {"pk": res.user.id }

                if len(res_activity) == 0: # Resource isn't booked at all
                        r['resource'] = '''%s - Available all day''' % res_full_name
                        r['available'] = True
                        logging.debug('''%s has no Engineering Days booked.''' % res)
                
                elif len(res_activity) >= 2: # User already has 2 bookings for this day
                        r['resource'] = '''%s - Booked out all day''' % res_full_name
                        r['available'] = False
                        logging.debug('''%s has 2 Engineering Days booked: %s.''' % ( res, res_activity ))
                else:
                        for day in res_activity:
                                if day.day_type == 0:
                                        r['resource'] = '''%s - Available PM only''' % res_full_name
                                        r['available'] = True
                                        logging.debug('''%s is available in PM. Booked on %s in AM.''' % ( res, day ))
                                elif day.day_type == 1:
                                        r['resource'] = '''%s - Available AM only''' % res_full_name
                                        r['available'] = True
                                        logging.debug('''%s is available in AM. Booked on %s in PM.''' % ( res, day ))
                                elif day.day_type == 2:
                                        r['resource'] = '''%s - Booked out all day''' % res_full_name
                                        r['available'] = False
                                        logging.debug('''%s has no availability. Booked on %s.''' % ( res, day ))


                try:
                        rota = RotaItem.objects.get(person=res.user, date=requested_date)
                        if rota.activity.unavailable_for_projects:
                                r['resource'] = '''%s - Not Available''' % res_full_name
                                r['available'] = False
                                logging.debug('''%s has no availability. Rota'd on %s.''' % ( res, rota ))
                except RotaItem.DoesNotExist:
                        pass
                                
                
                ret.append(r)
        if as_json:
                return HttpResponse(json.dumps(ret))
        else:
                return ret
                                

@login_required
def add_engineering_day(request, project_number, wbs_id):

        project = get_object_or_404(Project, project_number=project_number)
        check_project_write_acl(project, request.user)  # Will return Http404 if user isn't allowed to view project
        work_item = WorkItem.objects.get(id=wbs_id)
                
        if request.method == 'POST':
                form = EngineeringDayForm(request.POST)
                if form.is_valid():
                        t = form.save(commit=False)     
                        logging.debug('''resource => %s, work_date => %s, day_type => %s''' % ( t.resource, t.work_date, t.day_type ))
                        
                        available_resources = get_resources_for_engineering_day(request, project_number, wbs_id, t.work_date.strftime("%Y"), t.work_date.strftime("%m"), t.work_date.strftime("%d"), t.day_type, as_json=False)
                        logging.debug('''Resource ID is: %s''' % t.resource.id )
                        logging.debug('''Available resources are: %s''' % available_resources )
                        if t.resource.id not in [ r['pk'] for r in available_resources ]:
                                logging.debug('''User has tried to book %s on %s when he hasn't got the correct skillset''' % ( t.resource, t.work_date ))
                                return HttpResponse( handle_generic_error("Sorry - this resource hasn't got the skillset to work on this task"))

                        if EngineeringDay.objects.filter(work_date=t.work_date, resource=t.resource, day_type__in=[ t.day_type, 2]).count() > 0:
                                logging.debug('''User has tried to book %s on %s when he has existing engineering days booked''' % ( t.resource, t.work_date ))
                                return HttpResponse( handle_generic_error("Sorry - this resource is already booked at this time."))
                                
                        
                        
                        t.save()
                        work_item.engineering_days.add(t)
                        work_item.save()
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))
        
@login_required
def view_wbs(request, project_number):
        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
        wbs = project.work_items.all()
        # Data cleaning, ExtJS grids can't load if some ForiegnKey fields are Null
        for w in wbs:
                if not w.depends:
                        w.depends = WorkItem(title='')
                try:
                        i = w.owner
                except User.DoesNotExist: 
                        w.owner = User()
        
        
        return HttpResponse( serializers.serialize('json', wbs, relations={'depends': {'fields': ('title',)}, 'skill_set': {'fields': ('skill',)}, 'project_stage': {'fields': ('stage',)},'author': {'fields': ('id', 'username'), 'extras': ('get_full_name',)},'owner': { 'fields': ('id', 'username'), 'extras': ('get_full_name',)}}, extras=('get_work_item_status',)))
        
@login_required
def view_work_item(request, project_number, wbs_id):
        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
        work_item = WorkItem.objects.get(id=wbs_id)

        # Some error checking
        if not work_item.depends:
                work_item.depends = WorkItem(title='')
        try:
                i = work_item.owner
        except User.DoesNotExist: 
                work_item.owner = User()
        
        


        JSONSerializer = serializers.get_serializer('json')
        j = JSONSerializer()
        if work_item.start_date != None: work_item.start_date = work_item.start_date.strftime("%d/%m/%Y")
        if work_item.finish_date != None: work_item.finish_date = work_item.finish_date.strftime("%d/%m/%Y")
        j.serialize([work_item], fields=('skill_set', 'project_stage', 'title', 'description', 'depends', 'duration', 'owner', 'percent_complete', 'start_date', 'finish_date', 'wbs_number', 'cost', 'history', 'engineering_days'))
        return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))

        return HttpResponse( serializers.serialize('json', WorkItem.objects.filter(id=wbs_id), relations=('author', 'owner')))  

@login_required
def get_timeline(request, project_number):
    project = get_object_or_404(Project, project_number=project_number)
    check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project

    t_format = "%a %d %b %Y %H:%M:%S +0000"

    ret = {}
    ret['events'] = []
    for w in project.work_items.all():
        dict = {}
        do_not_append = False
        if w.start_date and w.duration:
            dict['start'] = w.start_date.strftime(t_format)
            dict['durationEvent'] = True
            if project.duration_type == 0: # Hours
                end = w.start_date + datetime.timedelta(hours=w.duration)
                dict['end']  = end.strftime(t_format)
            elif project.duration_type == 1: # Days
                end = w.start_date + datetime.timedelta(days=w.duration)
                dict['end']  = end.strftime(t_format)

        elif w.finish_date and w.duration:
            dict['end'] = w.finish_date.strftime(t_format)
            dict['durationEvent'] = True
            if project.duration_type == 0: # Hours
                end = w.finish_date + datetime.timedelta(hours=-w.duration)
                dict['start']  = end.strftime(t_format)
            elif project.duration_type == 1: # Days
                end = w.finish_date + datetime.timedelta(days=-w.duration)
                dict['start']  = end.strftime(t_format)
        elif w.start_date and w.finish_date:
            dict['start'] = w.start_date.strftime(t_format)
            dict['end'] = w.finish_date.strftime(t_format)
            dict['durationEvent'] = True

        else:
            do_not_append = True # Can't add to Timeline
        dict['title'] = w.title
        dict['description'] = w.description
        rag_status = get_task_rag_status(w)
        if rag_status == 'rag_status_red':
            dict['color'] = '#ff0000'
        elif rag_status == 'rag_status_amber':
            dict['color'] = '#ff9900'
        if w.percent_complete == 100:
            dict['color'] = '#00ff00'

        if not do_not_append:
            ret['events'].append(dict)
    return HttpResponse( json.dumps(ret) )

@login_required
def get_jsgantt_xml(request, project_number):
    project = get_object_or_404(Project, project_number=project_number)
    check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
    #t_format = "%a %d %b %Y %H:%M:%S +0000"
    t_format = "%m/%d/%Y"

    from xml.dom.minidom import Document
    doc = Document()
    xml_project = doc.createElement("project")
    doc.appendChild(xml_project)
    for w in project.work_items.all():
        task = doc.createElement("task")
        xml_project.appendChild(task)

        pID = doc.createElement("pID")
        pID.appendChild( doc.createTextNode(str(w.wbs_number)) )
        task.appendChild(pID)

        pName = doc.createElement("pName")
        pName.appendChild( doc.createTextNode(w.title))
        task.appendChild(pName)

        pStart = doc.createElement("pStart")
        pEnd = doc.createElement("pEnd")
        pMile = doc.createElement("pMile")

        if w.start_date and w.finish_date:
            start_date = w.start_date.strftime(t_format)
            finish_date = w.finish_date.strftime(t_format)
            mile = "0"
        elif w.start_date and w.duration:
            start_date =  w.start_date.strftime(t_format)
            mile = "0"
            if project.duration_type == 0: # Hours
                finish_date = (w.start_date + datetime.timedelta(hours=w.duration)).strftime(t_format)
            elif project.duration_type == 1: # Days
                finish_date = (w.start_date + datetime.timedelta(days=w.duration)).strftime(t_format)
        elif w.finish_date and w.duration:
            finish_date = w.finish_date.strftime(t_format)
            mile = "0"
            if project.duration_type == 0: # Hours
                start_date = (w.finish_date + datetime.timedelta(hours=-w.duration)).strftime(t_format)
            elif project.duration_type == 1: # Days
                start_date = (w.finish_date + datetime.timedelta(days=-w.duration)).strftime(t_format)
        else:
            if w.start_date:
                start_date = w.start_date.strftime(t_format)
                finish_date = w.start_date.strftime(t_format)
            elif w.finish_date:
                start_date = w.finish_date.strftime(t_format)
                finish_date = w.finish_date.strftime(t_format)
            mile = "1"
        pStart.appendChild( doc.createTextNode(start_date))
        task.appendChild(pStart)
        pEnd.appendChild( doc.createTextNode(finish_date))
        task.appendChild(pEnd)
        pMile.appendChild( doc.createTextNode(mile))
        task.appendChild(pMile)

        pRes = doc.createElement("pRes")
        pRes.appendChild( doc.createTextNode(w.owner.get_full_name()))
        task.appendChild(pRes)

        if w.percent_complete:
            pComp = doc.createElement("pComp")
            pComp.appendChild( doc.createTextNode(str(w.percent_complete)))
            task.appendChild(pComp)
        if w.depends:
            pDepend = doc.createElement("pDepend")
            pDepend.appendChild( doc.createTextNode(str(w.depends.wbs_number)))
            task.appendChild(pDepend)


    print doc.toprettyxml()
    return HttpResponse(doc.toprettyxml(), mimetype="text/xml")
            

            
            
@login_required
def view_gantt_chart(request, project_number):
    project = get_object_or_404(Project, project_number=project_number)
    check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
    return render_to_response('wbs/gantt.html', { 'project': project }, context_instance=RequestContext(request))
    
