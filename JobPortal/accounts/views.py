from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile  # Import the profile model
from .forms import RegistrationForm

def index(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('index')
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            gender = form.cleaned_data['gender']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if passwords match
            if password != confirm_password:
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Passwords do not match'
                })

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Username already exists'
                })

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Email already exists'
                })

            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create the user profile
            UserProfile.objects.create(
                user=user,
                role=role,
                phone_number=phone_number,
                gender=gender
            )

            # Log the user in
            auth_login(request, user)
            return redirect('home')
        else:
            # Form is invalid
            return render(request, 'register.html', {
                'form': form,
                'error': 'Please correct the errors below'
            })

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return render(request, 'login.html', {'error': 'All fields are required'})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

        # Log the user in
        auth_login(request, user)
        return redirect('home')
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')
