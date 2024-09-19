from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from teacher.models import Category
from .forms import LoginForm, SignupForm

def home(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, "home/landing_page.html", context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Check the user's role and redirect accordingly
                if user.userprofile.role == 'teacher':
                    return redirect('teacher_dashboard')  # Redirect to teacher dashboard
                elif user.userprofile.role == 'student':
                    return redirect('student_dashboard')  # Redirect to student dashboard
                else:
                    return redirect('home')  # Fallback redirect
                
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'home/login_page.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Automatically assign the role of 'student' upon signup
            user.userprofile.role = 'student'
            user.userprofile.save()

            # Authenticate and log in the user
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Account created and logged in successfully!')
                return redirect('student_dashboard')  # Redirect to student dashboard after successful signup
    else:
        form = SignupForm()
    
    return render(request, 'home/signup_page.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('landing')  # Replace 'landing' with your landing page URL name

