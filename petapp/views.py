import os, requests
from django.db.models import Q
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, PetPost, Message # added
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# * Variables *
User = get_user_model()
api_url_division = "https://bdapis.com/api/v1.2/divisions"


# ** Provides Posts **
def fetchAdoptedPost(total=False):
  posts = []
  
  if total:
    posts = PetPost.objects.filter(status='Adopted').order_by('-updated_at')[:total]
  else:
    posts = PetPost.objects.filter(status='Adopted').order_by('-updated_at')
    
  return posts


# ** Provides Posts **
def fetchPost(total=False):
  posts = []
  
  if total:
    posts = PetPost.objects.filter(status='Active').order_by('-created_at')[:total]
  else:
    posts = PetPost.objects.filter(status='Active').order_by('-created_at')
  
  return posts


# ** Provides Message **
def fetchMessage(total=False):
  message = []
  
  if total:
    message = Message.objects.all().order_by('-created_at')[:total]
  else:
    message = Message.objects.all().order_by('-created_at')
  
  return message


# ** Homepage **
def home(request):
  active_posts = fetchPost(6)
  adopted_posts = fetchAdoptedPost(4)

  response = requests.get(api_url_division)
  if response.status_code == 200:
      divisions_data = response.json().get("data", [])
  else:
      divisions_data = []
  
  return render(request, 'petapp/index.html', {'posts': active_posts, 'adoptedPosts': adopted_posts, 'divisions': divisions_data})


# ** Profile **
def userProfile(request, userid):
  user = get_object_or_404(UserProfile, id=userid)
  posts_list = PetPost.objects.filter(user=user).order_by('-created_at')
  
  paginator = Paginator(posts_list, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  if request.method == 'POST':
    message_content = request.POST.get('message')
    if message_content:
        # Prepare the message fields
        message_data = {
            'sender': request.user,
            'receiver': user,
            'message': message_content,
        }
        
        # Create the message
        Message.objects.create(**message_data)

        messages.success(request, "Your message has been sent to the pet post publisher.")
        return redirect('userprofile', userid=userid)
    else:
        messages.error(request, "Message content cannot be empty.")
  
  return render(request, 'petapp/userprofile.html', {'user': user, 'page_obj': page_obj, 'isPost': len(page_obj) > 0})


# ** Login **
def user_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid email or password.")
        return render(request, 'petapp/login.html')

    user = authenticate(request, username=user.username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, "Invalid email or password.")
        return render(request, 'petapp/login.html')

  return render(request, 'petapp/login.html')


# ** Registration **
def registration(request):
  if request.method == 'POST':
    form_data = {
        'username': request.POST.get('username'),
        'first_name': request.POST.get('firstName'),
        'last_name': request.POST.get('lastName'),
        'email': request.POST.get('emailAddress'),
        'phone1': request.POST.get('phone1'),
        'phone2': request.POST.get('phone2'),
        'socialLink': request.POST.get('socialLink'),
        'address': request.POST.get('address'),
        'state': request.POST.get('state'),
    }
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if not form_data['first_name'] or not form_data['last_name'] or not form_data['address'] or not form_data['state']:
        messages.error(request, "First name, last name, address, and state cannot be empty.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
      
    if ' ' in form_data['username'] or not form_data['username'].islower():
        messages.error(request, "Username cannot contain spaces or uppercase letters.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    
    if not (form_data['phone1'].isdigit() and len(form_data['phone1']) == 11):
        messages.error(request, "Primary phone number must contain exactly 11 digits.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    if form_data['phone2'] and (not form_data['phone2'].isdigit() or len(form_data['phone2']) != 11):
        messages.error(request, "Additional phone number must contain exactly 11 digits.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    
    url_validator = URLValidator()
    try:
        url_validator(form_data['socialLink'])
    except ValidationError:
        messages.error(request, "Social link must be a valid URL.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
          
    if len(password1) < 6:
        messages.error(request, "Password must be at least 6 characters long.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})

    if password1 != password2:
        messages.error(request, "Passwords do not match.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})

    if User.objects.filter(username=form_data['username']).exists():
        messages.error(request, "Username already taken.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    if User.objects.filter(email=form_data['email']).exists():
        messages.error(request, "Email already taken.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})

    user = User(
      username=form_data['username'],
      first_name=form_data['first_name'],
      last_name=form_data['last_name'],
      email=form_data['email'],
      phone_number=form_data['phone1'],
      additional_number=form_data['phone2'],
      social_media_link=form_data['socialLink'],
      address=form_data['address'],
      state=form_data['state'],
      password=make_password(password1)
    )
    user.save()
    messages.success(request, f'Account created for {form_data["username"]}!')
    return redirect('login')

  return render(request, 'petapp/registration.html')


# ** About Us **
def about(request):
  return render(request, 'petapp/about.html')

# ** All Items **
def items(request):
  division = request.GET.get('division')
  district = request.GET.get('district')
  search_query = request.GET.get('query')
  
  pet_type = request.GET.get('type')
  api_url_for_district = f"https://bdapis.com/api/v1.2/division/{division}" if division else None
  
  response = requests.get(api_url_division)
  if response.status_code == 200:
      divisions_data = response.json().get("data", [])
  else:
      divisions_data = []

  districts_data = []
  if division and api_url_for_district:
      district_response = requests.get(api_url_for_district)
      if district_response.status_code == 200:
          districts_data = district_response.json().get("data", [])
  
  posts_list = PetPost.objects.all().filter(status="Active").order_by('-created_at')
  if pet_type:
      posts_list = posts_list.filter(pet_type__iexact=pet_type)
      
  if division:
      posts_list = posts_list.filter(division__iexact=division)
      
  if district:
      posts_list = posts_list.filter(district__iexact=district)

  if search_query:
      # Filter posts by the search query (e.g., title or description)
      posts_list = posts_list.filter(
          Q(title__icontains=search_query) | Q(description__icontains=search_query)
      )
        
  paginator = Paginator(posts_list, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
      'divisions': divisions_data,
      'selected_division': division,
      'districts': districts_data,
      'posts': posts_list,
      'page_obj': page_obj,
      'selected_type': pet_type,
  }

  return render(request, 'petapp/items.html', context)

  
# ** Single Pet Post **
def item(request, id):
  posts = PetPost.objects.exclude(id=id).order_by('-created_at')[:2]
  pet = get_object_or_404(PetPost, id=id)

  if request.method == 'POST':
    message_content = request.POST.get('message')
    if message_content:
      Message.objects.create(
        sender=request.user,
        receiver=pet.user,
        pet_post=pet,
        message=message_content
      )
      messages.success(request, "Your message has been sent to the pet post publisher.")
      return redirect('item', id=id)
    else:
        messages.error(request, "Message content cannot be empty.")

  return render(request, 'petapp/item.html', {'pet': pet, 'division': pet.division, 'district': pet.district, 'posts': posts})


# ** Disctricts **
def get_districts(request):
  division = request.GET.get('division')
  if division:
      # Fetch districts based on the selected division
      api_url_for_district = f"https://bdapis.com/api/v1.2/division/{division}"
      response = requests.get(api_url_for_district)
      if response.status_code == 200:
          districts_data = response.json().get("data", [])
          return JsonResponse({'districts': districts_data}, status=200)
  return JsonResponse({'districts': []}, status=400)


# ** Pet Post Creation **
@login_required
def createPet(request):
  # Fetch divisions data
  response = requests.get(api_url_division)
  if response.status_code == 200:
      divisions_data = response.json().get("data", [])
  else:
      divisions_data = []

  if request.method == 'POST':
      title = request.POST.get('title')
      image = request.FILES.get('image')
      pet_type = request.POST.get('type')
      gender = request.POST.get('gender')
      description = request.POST.get('description')
      age = request.POST.get("age")
      
      division = request.POST.get('division')
      district = request.POST.get('district')

      pet_post = PetPost(
          user=request.user,
          title=title,
          image=image,
          pet_type=pet_type,
          gender=gender,
          description=description,
          division=division,
          district=district,
          age=age,
      )

      pet_post.save()
      return redirect('home')

  return render(request, 'petapp/createPet.html', {"divisions": divisions_data})


# ** Logout **
def user_logout(request):
  logout(request)
  return redirect('login')

# ** Dashboard of user **
@login_required
def dashboard(request):
  totalPost = len(PetPost.objects.filter(user=request.user))
  totalMessage = len(fetchMessage())
  totalAdopted = len(fetchAdoptedPost())
  
  return render(request, 'Dashboard/Dashboard.html', {"totalAdopted":totalAdopted, 'current_page':'dashboard', "totalPost": totalPost, "totalMessage": totalMessage, "fullname": request.user.first_name + " " + request.user.last_name})


# ** Message Requests **
@login_required
def totalRequest(request):
  messages = Message.objects.filter(receiver=request.user).order_by('-created_at')[:10]
  
  return render(request, 'Dashboard/TotalRequest.html', {'posts': messages, 'current_page':'totalRequest' ,"fullname": request.user.first_name + " " + request.user.last_name})


# ** Information Update **
@login_required
def updateInfo(request):
    user = request.user

    if request.method == 'POST':
      username = request.POST.get('username', user.username)
      first_name = request.POST.get('first_name', user.first_name)
      last_name = request.POST.get('last_name', user.last_name)
      email = request.POST.get('email', user.email)
      phone1 = request.POST.get('phone1', user.phone_number) 
      phone2 = request.POST.get('phone2', user.additional_number)
      address = request.POST.get('address', user.address)
      state = request.POST.get('state', user.state)
      social_link = request.POST.get('social_link', user.social_media_link)

      current_password = request.POST.get('current_password')
      new_password = request.POST.get('new_password')
      confirm_password = request.POST.get('confirm_password')

      user.username = username
      user.first_name = first_name
      user.last_name = last_name
      user.email = email
      user.phone_number = phone1
      user.additional_number = phone2
      user.address = address
      user.state = state
      user.social_media_link = social_link

      if current_password and new_password and confirm_password:
        if check_password(current_password, user.password):
            if new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully.')
            else:
                messages.error(request, 'New password and confirmation do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

      user.save()

      messages.success(request, 'Information updated successfully.')
      return redirect('updateInfo')

    context = {
      'username': user.username,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
      'phone1': user.phone_number,
      'phone2': user.additional_number,
      'address': user.address,
      'state': user.state,
      'social_link': user.social_media_link,
    }
    return render(request, 'Dashboard/UpdateInfo.html', {"user":context, 'current_page':'updateInfo'})


# ** Pet Post Update **
@login_required
def updatePet(request, pet_id):
  
  user = request.user
  pet = get_object_or_404(PetPost, id=pet_id)

  response = requests.get(api_url_division)
  if response.status_code == 200:
      divisions_data = response.json().get("data", [])
  else:
      divisions_data = []

  if pet.user != user:
      messages.error(request, "You are not authorized to update this pet.")
      return redirect('dashboard')

  if request.method == 'POST':
      print("POST request received")
      title = request.POST.get('title', pet.title)
      pet_type = request.POST.get('pet_type', pet.pet_type)
      gender = request.POST.get('gender', pet.gender)
      # location = request.POST.get('location', pet.location)
      description = request.POST.get('description', pet.description)
      status = request.POST.get('status', pet.status)
      division = request.POST.get('division', pet.division)
      district = request.POST.get('district', pet.district)
      new_image = request.FILES.get('image')

      pet.title = title
      pet.pet_type = pet_type
      pet.gender = gender
      # pet.location = location
      pet.description = description
      pet.status = status
      pet.district = district
      pet.division = division
      
      if new_image:
          if pet.image and os.path.isfile(pet.image.path):
              os.remove(pet.image.path)
          pet.image = new_image

      pet.save()
      messages.success(request, "Pet updated successfully!")
      return redirect('totalPets')

  return render(request, 'Dashboard/updatePet.html', {'pet': pet , "divisions": divisions_data})

  
# ** All Posts **
@login_required
def totalPets(request):
  pets = PetPost.objects.filter(user=request.user).order_by('-created_at')[:10]
  
  return render(request, 'Dashboard/TotalPets.html', {'posts': pets, 'current_page':'myPets', "fullname": request.user.first_name + " " + request.user.last_name})


# ** Delete Message **
def delete_message(request, message_id):
  message = get_object_or_404(Message, id=message_id)
 
  if request.user == message.receiver:
    message.delete()
    messages.success(request, "Message deleted successfully.")
  else:
    messages.error(request, "You don't have permission to delete this message.")
  return redirect('totalRequest')


# ** Delete Pet **
def delete_pet(request, pet_id):
  pet = get_object_or_404(PetPost, id=pet_id)
 
  if request.user == pet.user:
    pet.delete()
    messages.success(request, "Pet deleted successfully.")
  else:
    messages.error(request, "You don't have permission to delete this pet.")
    
  return redirect('totalPets')