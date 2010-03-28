from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from tinymce.widgets import TinyMCE
from projects.misc import all_username_options, all_company_options


class EditPID(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the PID '''

	class Meta:
		model = Project
		fields = ('project_name', 'project_number', 'project_status', 'company', 'project_manager', 'team_managers', 'project_sponsor', 'project_description',
					'business_case', 'business_benefits', 'project_scope', 'exclusions', 'assumptions',
					'communications_plan', 'quality_plan')


class DialogEditCompany(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the company a project belongs to. '''

	class Meta:
		model = Project
		fields = ('company',)
	def __init__(self, *args, **kwargs):
		super(DialogEditCompany, self).__init__(*args, **kwargs)
		self.fields['company'].choices = all_company_options()
	
class DialogEditProjectManager(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the PM for a project. '''

	class Meta:
		model = Project
		fields = ('project_manager',)

	def __init__(self, *args, **kwargs):
		super(DialogEditProjectManager, self).__init__(*args, **kwargs)
		self.fields['project_manager'].choices = all_username_options()
	
class DialogEditTeamManagers(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Team Managers for a project. '''

	class Meta:
		model = Project
		fields = ('team_managers',)
	
	def __init__(self, *args, **kwargs):
		super(DialogEditTeamManagers, self).__init__(*args, **kwargs)
		self.fields['team_managers'].choices = all_username_options()

class DialogEditProjectSponsor(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Sponsor for a project. '''

	class Meta:
		model = Project
		fields = ('project_sponsor',)
	
	def __init__(self, *args, **kwargs):
		super(DialogEditProjectSponsor, self).__init__(*args, **kwargs)
		self.fields['project_sponsor'].choices = all_username_options()

class DialogEditProjectDescription(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Project Description '''

	class Meta:
		model = Project
		fields = ('project_description',)
	

class DialogEditBusinessCase(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Business Case'''

	class Meta:
		model = Project
		fields = ('business_case',)
	
class DialogEditBusinessBenefits(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Business Benefits'''

	class Meta:
		model = Project
		fields = ('business_benefits',)
	
class DialogEditProjectScope(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Project Scope'''

	class Meta:
		model = Project
		fields = ('project_scope',)
	
class DialogEditExclusions(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Project Exclusions'''

	class Meta:
		model = Project
		fields = ('exclusions',)
	
class DialogEditAssumptions(ModelForm):
	
	''' Used in templates/projects/view-project.html to edit the Project Assumption'''

	class Meta:
		model = Project
		fields = ('assumptions',)
	
class DialogExecutiveSummary(ModelForm):

	''' Used in templates/projects/view-project.html to provide an executive summary '''

	class Meta:
		model = ExecutiveSummary
		fields = ('summary','author','type')

	def __init__(self, *args, **kwargs):
		super(DialogExecutiveSummary, self).__init__(*args, **kwargs)
		self.fields['author'].widget = HiddenInput()
		self.fields['type'].widget = HiddenInput()

















