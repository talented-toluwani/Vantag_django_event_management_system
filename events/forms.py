from django.forms import ModelForm
from django import forms

from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
        "title", 
        "description", 
        "location", 
        "date", 
        "capacity", 
        "category",
        ]
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False)
    urgent = forms.BooleanField(required=False)


    