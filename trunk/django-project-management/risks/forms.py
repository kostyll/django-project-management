from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from risks.models import *
#from misc.widgets import DateTimeWidget
#from backends.authlib import *


class RiskForm(ModelForm):
        
        class Meta:
                model = Risk
                fields = ('description', 'owner', 'probability', 'impact', 'counter_measure', 'status',)
