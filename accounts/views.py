from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registering
            django_login(request, user)
            return redirect('profile_view')  # Assuming you have a view named 'profile_view'
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            return redirect('profile_view')
        else:
            # Add this to show the custom error message when form is not valid
            form.add_error(None, "Username or password is invalid")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    django_logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    return JsonResponse(data)

@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Only set the password if password1 is not empty
        if password1:
            if password1 != password2:
                return render(request, 'profile_edit.html', {
                    'error': "The two password fields didn't match."
                })
            if len(password1) < 8:
                return render(request, 'profile_edit.html', {
                    'error': "This password is too short. It must contain at least 8 characters."
                })
            user.set_password(password1)
            user.save()

        return redirect('profile_view')

    return render(request, 'accounts/profile_edit.html', {
        'user': user
    })