from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
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

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email')
    