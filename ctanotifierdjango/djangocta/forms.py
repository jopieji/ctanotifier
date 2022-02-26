from typing import Text
from django.forms import ModelForm, TextInput
from .models import Stops

class StopForm(ModelForm):
    class Meta:
        model = Stops
        fields = ['stop']
        widgets = {'stop': TextInput(attrs={ 'class' : 'input', 'placeholder' : 'Stop Name'})}