from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import UserProfile, PetPost, Message # added
from django.contrib.auth.decorators import login_required

User = get_user_model()

def fetchPost(total):
  posts = PetPost.objects.all().order_by('-created_at')[:total]
  
  return posts

def home(request):
  posts = fetchPost(6)

  return render(request, 'petapp/index.html', {'posts': posts})

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
        return redirect('home')  # Redirect to the home page or any other page after login
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
  posts = fetchPost(10)
  
  # pagination 
  posts_list = PetPost.objects.all().order_by('-created_at')
  paginator = Paginator(posts_list, 10)
  
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
    
  return render(request, 'petapp/items.html', {'posts': posts, 'page_obj': page_obj})

def item(request, id):
  posts = PetPost.objects.exclude(id=id).order_by('-created_at')[:2]
  pet = get_object_or_404(PetPost, id=id)

  # started
  if request.method == 'POST':
    # Get the message content from the form
    message_content = request.POST.get('message')
    print(request.user)
    if message_content:
      Message.objects.create(
        sender=request.user,
        receiver=pet.user,
        pet_post=pet,
        message=message_content
      )
      messages.success(request, "Your message has been sent to the pet post publisher.")
      return redirect('item', id=id)  # Redirect to avoid resubmission on refresh
    else:
        messages.error(request, "Message content cannot be empty.")

  return render(request, 'petapp/item.html', {'pet': pet, 'posts': posts})

# def modal(request):
#   return render(request, 'petapp/modal.html')

@login_required
def createPet(request):
  if request.method == 'POST':
      title = request.POST.get('title')
      image = request.FILES.get('image')
      pet_type = request.POST.get('pet_type')
      gender = request.POST.get('gender')
      description = request.POST.get('description')
      location = request.POST.get('location')

      pet_post = PetPost(
          user=request.user,
          title=title,
          image=image,
          pet_type=pet_type,
          gender=gender,
          description=description,
          location=location,
      )

      pet_post.save()

      return redirect('home')

  return render(request, 'petapp/createPet.html')

def user_logout(request):
  logout(request)
  return redirect('login')

# Dashboard

def Dashboard(request):
  return render(request, 'Dashboard/Dashboard.html')