from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout
from .models import JobSeeker, Recruiter
from .forms import RegistrationForm

def index(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('index')
    
    return render(request, 'index.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
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

            if password != confirm_password:
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Passwords do not match'
                })

            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Username already exists'
                })

            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Email already exists'
                })

            if JobSeeker.objects.filter(phone_number=phone_number).exists() or \
               Recruiter.objects.filter(phone_number=phone_number).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Phone number already exists'
                })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            if role == 'jobseeker':
                JobSeeker.objects.create(
                    user=user,
                    phone_number=phone_number,
                    gender=gender
                )
            else:
                Recruiter.objects.create(
                    user=user,
                    phone_number=phone_number,
                    gender=gender
                )

            auth_login(request, user)
            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return render(request, 'login.html', {'error': 'All fields are required'})

        user = User.objects.filter(username=username).first()

        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        
        if not user.check_password(password):
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        
        auth_login(request, user)
        return redirect('home')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')



