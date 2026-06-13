from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

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
