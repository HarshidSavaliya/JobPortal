from django.shortcuts import render, redirect
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User as UserProfile , RecruiterProfile, JobSeekerProfile
from .forms import RegistrationForm , LoginForm , UpdateUserProfileForm , UpdateJobSeekerProfileForm , UpdateRecruiterProfileForm
from django.contrib import messages




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
            if AuthUser.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Username already exists'
                })

            # Check if email already exists
            if AuthUser.objects.filter(email=email).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Email already exists'
                })

            # Create the user
            auth_user = AuthUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create the user profile
            profile = UserProfile.objects.create(
                user=auth_user,
                role=role,
                email=email,
                phone_number=phone_number,
                gender=gender
            )

            if role == 'recruiter':
                RecruiterProfile.objects.create(
                    user_profile=profile
                )
            else:
                JobSeekerProfile.objects.create(
                    user=profile
                )

            request.session['role'] = role

            # Log the user in
            auth_login(request, auth_user)
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
        auth_user = authenticate(request, username=username, password=password)

        if auth_user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

        # Log the user in
        auth_login(request, auth_user)
        if hasattr(auth_user, 'profile'):
            request.session['role'] = auth_user.profile.role
        return redirect('home')
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required(login_url='login')
def update_profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile record does not exist for this account.')
        return redirect('home')
    jobseeker_form = None
    recruiter_form = None

    if request.method == 'POST':
        user_form = UpdateUserProfileForm(request.POST, instance=user_profile)

        if user_profile.role == 'jobseeker':
            jobseeker_profile, _ = JobSeekerProfile.objects.get_or_create(user=user_profile)
            jobseeker_form = UpdateJobSeekerProfileForm(
                request.POST,
                request.FILES,
                instance=jobseeker_profile,
            )
            if user_form.is_valid() and jobseeker_form.is_valid():
                user_form.save()
                jobseeker_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('home')
        elif user_profile.role == 'recruiter':
            recruiter_profile, _ = RecruiterProfile.objects.get_or_create(user_profile=user_profile)
            recruiter_form = UpdateRecruiterProfileForm(
                request.POST,
                request.FILES,
                instance=recruiter_profile,
            )
            if user_form.is_valid() and recruiter_form.is_valid():
                user_form.save()
                recruiter_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('home')
        else:
            messages.error(request, 'Invalid role for profile update.')
            return redirect('home')
    else:
        user_form = UpdateUserProfileForm(instance=user_profile)

        if user_profile.role == 'jobseeker':
            jobseeker_profile, _ = JobSeekerProfile.objects.get_or_create(user=user_profile)
            jobseeker_form = UpdateJobSeekerProfileForm(instance=jobseeker_profile)
        elif user_profile.role == 'recruiter':
            recruiter_profile, _ = RecruiterProfile.objects.get_or_create(user_profile=user_profile)
            recruiter_form = UpdateRecruiterProfileForm(instance=recruiter_profile)
        else:
            messages.error(request, 'Invalid role for profile update.')
            return redirect('home')

    return render(
        request,
        'update_profile.html',
        {
            'user_form': user_form,
            'jobseeker_form': jobseeker_form,
            'recruiter_form': recruiter_form,
        },
    )
