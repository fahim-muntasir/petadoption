from django.shortcuts import render

def home(request):
  return render(request, 'petapp/index.html')

def login(request):
  return render(request, 'petapp/login.html')

def registration(request):
  return render(request, 'petapp/registration.html')

def about(request):
  return render(request, 'petapp/about.html')

def items(request):
  return render(request, 'petapp/items.html')

def item(request):
  return render(request, 'petapp/item.html')

def createPet(request):
  return render(request, 'petapp/createPet.html')