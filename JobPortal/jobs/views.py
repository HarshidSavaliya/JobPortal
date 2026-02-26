from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job
from accounts.models import RecruiterProfile, User as UserProfile


@login_required(login_url='login')
def post_job(request):
    try:
        recruiter_profile = RecruiterProfile.objects.get(user_profile__user=request.user)
    except RecruiterProfile.DoesNotExist:
        messages.error(request, 'You need to be a recruiter to post a job.')
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            Job.objects.create(recruiter=recruiter_profile, **form.cleaned_data)
            messages.success(request, 'Job posted successfully.')
            return redirect('home')
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})


