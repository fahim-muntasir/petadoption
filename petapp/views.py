from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import UserProfile # added

User = get_user_model()

def home(request):
  return render(request, 'petapp/index.html')

def user_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Find the user by email
    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid email or password.")
        return render(request, 'users/login.html')

    # Authenticate user
    user = authenticate(request, username=user.username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'petapp/index.html')  # Redirect to the home page or any other page after login
    else:
        messages.error(request, "Invalid email or password.")
        return render(request, 'petapp/login.html')

  return render(request, 'petapp/login.html')

def registration(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    first_name = request.POST.get('firsName')
    last_name = request.POST.get('lastName')
    email = request.POST.get('emailAddress')
    phone1 = request.POST.get('phone1')
    phone2 = request.POST.get('phone2')
    socialLink = request.POST.get('socialLink')
    address = request.POST.get('address')
    state = request.POST.get('state')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    
    print(username, first_name, last_name, email, phone1, phone2, socialLink, address, state, password1, password2)

    if password1 != password2:
        messages.error(request, "Passwords do not match.")
        return render(request, 'petapp/registration.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already taken.")
        return render(request, 'petapp/registration.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already taken.")
        return render(request, 'petapp/registration.html')

    user = User(username=username, first_name=first_name, last_name=last_name,email=email, phone_number=phone1, additional_number=phone2,social_media_link=socialLink, address=address, state=state, password=make_password(password1))
    user.save()
    messages.success(request, f'Account created for {username}!')
    return redirect('login')

  return render(request, 'petapp/registration.html')

def about(request):
  return render(request, 'petapp/about.html')

def items(request):
  return render(request, 'petapp/items.html')

def item(request):
  return render(request, 'petapp/item.html')

def createPet(request):
  return render(request, 'petapp/createPet.html')

def user_logout(request):
  logout(request)
  return redirect('login')