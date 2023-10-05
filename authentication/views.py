from django.shortcuts import render
from django.http import HttpResponse 

def home(request):
    return HttpResponse("Under construction")

def signup(request):
    return render(request, 'authentication/signup.html')

def signin(request):
    return render(request, 'authentication/signin.html')

def signout(request):
    pass
