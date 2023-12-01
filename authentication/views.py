from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from task_manager.models import Task
from authentication.forms import TaskForm

@login_required
def view_task(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'authentication/view_tasks.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('view_tasks')
    else:
        form = TaskForm()
        
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'authentication/add_task.html', {'tasks': tasks, 'form': form})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('view_tasks')
    
    else: 
        form = TaskForm(instance=task)
        
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'authentication/update_task.html', {'tasks': tasks, 'form': form})

@login_required
def delete_task(request, task_id):


def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists. Please enter a different username.")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "That email address already exists. Please enter a different email.")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username is to long, must be less than 10 characters.")
            
        if pass1 != pass2:
            messages.error(request, "Your passwords do not match. Please try again")
            
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "Your account has been sucessfully created")
        
        return redirect("signin")
        
    return render(request, 'authentication/signup.html')

def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
            
        else:
            messages.error(request, "Incorrect Credentials")
            return redirect('home')
    
    
    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully! ")
    return redirect('home')
