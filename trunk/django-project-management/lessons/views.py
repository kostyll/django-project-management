# Create your views here.
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
from lessons.forms import *
from projects.misc import check_project_read_acl, check_project_write_acl


@login_required
def add_lesson(request, project_number):

	project = Project.objects.get(project_number=project_number)
	lessons = LessonLearnt.objects.filter(project=project)
	if request.method == 'POST':
		form = LessonForm(request.POST)
		if form.is_valid():
			t = form.save()
			t.save()
			project.lessons_learnt.add(t)
			project.save()
			request.user.message_set.create(message='''Lesson %s Registered''' % t.id)
			updateLog(request, project_number, '''Lesson %s Registered''' % t.id)
			return HttpResponseRedirect(project.get_absolute_url())
		else:
			pass

@login_required
def edit_lesson(request, project_number, lesson_id):

	project = Project.objects.get(project_number=project_number)
	lesson = LessonLearnt.objects.get(id=lesson_id)
	if request.method == 'POST':
		form = LessonForm(request.POST, instance=lesson)
		if form.is_valid():
			t = form.save()
			t.save()
			request.user.message_set.create(message='''Lesson %s Edited''' % t.id)
			for change in form.changed_data:
				updateLog(request, project_number, '%s changed to %s' % ( change, eval('''t.%s''' % change)))
			return HttpResponseRedirect(project.get_absolute_url())
		else:
			pass



@login_required
def deleteLessonLearnt(request, projectNumber, lessonSlug):

	project = Project.objects.get(projectNumber=projectNumber)
	lesson = LessonLearnt.objects.get(slug=lessonSlug)
	project.lessonsLearnt.remove(lesson)
	request.user.message_set.create(message='''Lesson %s Deleted''' % lesson.slug )
	return HttpResponseRedirect('/Projects/%s/LessonsLearnt' % project.projectNumber)
	
			

		
@login_required
def view_lessons(request, project_number):
	project = Project.objects.get(project_number=project_number)
	check_project_read_acl(project, request.user)	# Will return Http404 if user isn't allowed to view project

	return HttpResponse( serializers.serialize('json', project.lessons_learnt.all(), relations=('author',)))
	
