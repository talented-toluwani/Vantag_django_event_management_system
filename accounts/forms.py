from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser
class SignupForm(UserCreationForm):
    email = forms.EmailField(label = "Your Email Address")
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('participant', 'Participant')
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
       