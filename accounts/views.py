from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SignupForm


def register(request):
    if request.method == 'POST':
        user_signup = SignupForm(request.POST)
        if user_signup.is_valid():
            user = user_signup.save(commit=False)
            user.email = user_signup.cleaned_data['email']
            role = user_signup.cleaned_data['role']

            if role == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            
            user.save()
            messages.success(request, 'Account successfully created')
            return redirect('login')
    
    else:
        user_signup = SignupForm()
    
    return render(request, 'accounts/register.html', {'form': user_signup})
