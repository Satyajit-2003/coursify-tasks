# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Job, JobApplication, CustomUser

def home(request):
    return render(request, 'index.html' , {'user': request.user})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'user': request.user})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user.username = user.username.lower()
            if user:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'user': request.user})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs, 'user': request.user})

def apply(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to apply for a job.")
        return redirect('login')
    
    if request.method == 'POST':
        job_id = request.POST['job_id']
        job = Job.objects.filter(id=job_id).first()
        if 'skills' not in request.POST:
            return render(request, 'apply.html', {'user': request.user, 'job': job})
        name = request.POST['name']
        email = request.POST['email']
        skills = request.POST['skills']
        resume = request.POST['resume']
        cv = request.POST['cv']
        candidate = CustomUser.objects.filter(username=request.user.username).first()
        application = JobApplication(candidate=candidate, name=name, email=email, job=job, skills=skills,
                                      resume=resume, cv=cv)
        application.save()
        messages.success(request, "Application submitted successfully!")

    return redirect('job_list')

def applications(request):
    if not request.user.is_authenticated:
        return redirect('login')
    applications = JobApplication.objects.filter(candidate = CustomUser.objects.filter(username=request.user.username).first())
    return render(request, 'applications.html', {'applications': applications, 'user': request.user})