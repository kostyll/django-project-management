from django.forms import *
from django.contrib.admin import widgets                                       
from rota.models import *


class RotaItemForm(ModelForm):
	
	class Meta:
		model = RotaItem
		exclude = ('description', 'author', 'person', 'date')
