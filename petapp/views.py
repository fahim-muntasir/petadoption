from django.shortcuts import render

def home(request):
  return render(request, 'petapp/index.html')

def login(request):
  return render(request, 'petapp/login.html')

def registration(request):
  return render(request, 'petapp/registration.html')