from django.contrib.auth.models import AbstractUser
from django.db import models

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

class CustomUser(AbstractUser, models.TextChoices):
    ADMIN = 'admin', "Admin"
    PARTICIPANT = 'participant', 'Participant'

    role = models.CharField(max_length=20, default= 'Participant')

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)

def register(request):
    if request.method == 'POST':
        user_signup = UserCreationForm(request.POST)
        if user_signup.is_valid():
            user_signup.save()
            messages.success(request, 'Account successfully created')
            return redirect('login')
    
    else:
        user_signup = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': user_signup})
