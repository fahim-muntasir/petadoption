import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, PetPost, Message # added
from django.contrib.auth.decorators import login_required

User = get_user_model()

def fetchPost(total=False):
  posts = []
  
  if total:
    posts = PetPost.objects.all().order_by('-created_at')[:total]
  else:
    posts = PetPost.objects.all().order_by('-created_at')
  
  return posts

def fetchMessage(total=False):
  message = []
  
  if total:
    message = Message.objects.all().order_by('-created_at')[:total]
  else:
    message = Message.objects.all().order_by('-created_at')
  
  return message

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
        return render(request, 'petapp/login.html')

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
    # Get form data
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

    # Validation checks
    
    # 6. Check if first name, last name, address, and state are not empty
    if not form_data['first_name'] or not form_data['last_name'] or not form_data['address'] or not form_data['state']:
        messages.error(request, "First name, last name, address, and state cannot be empty.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
      
    # 3. Check if username has no spaces or uppercase letters
    if ' ' in form_data['username'] or not form_data['username'].islower():
        messages.error(request, "Username cannot contain spaces or uppercase letters.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    
    # 4. Check if the phone numbers have exactly 11 digits
    if not (form_data['phone1'].isdigit() and len(form_data['phone1']) == 11):
        messages.error(request, "Primary phone number must contain exactly 11 digits.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    if form_data['phone2'] and (not form_data['phone2'].isdigit() or len(form_data['phone2']) != 11):
        messages.error(request, "Additional phone number must contain exactly 11 digits.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    
    # 5. Validate the social link to ensure it's a URL
    url_validator = URLValidator()
    try:
        url_validator(form_data['socialLink'])
    except ValidationError:
        messages.error(request, "Social link must be a valid URL.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
          
    # 1. Check if password has at least 6 characters
    if len(password1) < 6:
        messages.error(request, "Password must be at least 6 characters long.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})

    # 2. Check if both passwords match
    if password1 != password2:
        messages.error(request, "Passwords do not match.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})

    # 7. Check if username or email is already taken
    if User.objects.filter(username=form_data['username']).exists():
        messages.error(request, "Username already taken.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})
    if User.objects.filter(email=form_data['email']).exists():
        messages.error(request, "Email already taken.")
        return render(request, 'petapp/registration.html', {'form_data': form_data})

    # Create the user if all validations pass
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

@login_required
def dashboard(request):
  totalPost = len(fetchPost())
  totalMessage = len(fetchMessage())
  
  return render(request, 'Dashboard/Dashboard.html', {"totalPost": totalPost, "totalMessage": totalMessage, "fullname": request.user.first_name + " " + request.user.last_name})

@login_required
def totalRequest(request):
  messages = Message.objects.filter(receiver=request.user).order_by('-created_at')[:10]
  
  return render(request, 'Dashboard/TotalRequest.html', {'posts': messages, "fullname": request.user.first_name + " " + request.user.last_name})

@login_required
def updateInfo(request):
    # Load the current user profile
    user = request.user

    if request.method == 'POST':
      # Get form data from POST request
      username = request.POST.get('username', user.username)
      first_name = request.POST.get('first_name', user.first_name)
      last_name = request.POST.get('last_name', user.last_name)
      email = request.POST.get('email', user.email)
      phone1 = request.POST.get('phone1', user.phone_number) 
      phone2 = request.POST.get('phone2', user.additional_number)
      address = request.POST.get('address', user.address)
      state = request.POST.get('state', user.state)
      social_link = request.POST.get('social_link', user.social_media_link)

      # Password change logic
      current_password = request.POST.get('current_password')
      new_password = request.POST.get('new_password')
      confirm_password = request.POST.get('confirm_password')

      # Update basic info
      user.username = username
      user.first_name = first_name
      user.last_name = last_name
      user.email = email
      user.phone_number = phone1
      user.additional_number = phone2
      user.address = address
      user.state = state
      user.social_media_link = social_link

      # Check if password fields are provided for a password update
      if current_password and new_password and confirm_password:
        # Verify current password
        if check_password(current_password, user.password):
            # Ensure new password matches confirmation
            if new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keeps the user logged in after password change
                messages.success(request, 'Password updated successfully.')
            else:
                messages.error(request, 'New password and confirmation do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

      # Save the user and profile info
      user.save()
      # user.profile.save()

      # Success message and redirect
      messages.success(request, 'Information updated successfully.')
      return redirect('updateInfo')

    # If GET request, pre-fill the form with current information
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
    return render(request, 'Dashboard/UpdateInfo.html', {"user": context})

@login_required
def totalPets(request):
  pets = PetPost.objects.filter(user=request.user).order_by('-created_at')[:10]
  
  return render(request, 'Dashboard/TotalPets.html', {'posts': pets, "fullname": request.user.first_name + " " + request.user.last_name})


def delete_message(request, message_id):

  message = get_object_or_404(Message, id=message_id)
 
  if request.user == message.receiver:
    message.delete()
    messages.success(request, "Message deleted successfully.")
  else:
    messages.error(request, "You don't have permission to delete this message.")
  return redirect('totalRequest')

def delete_pet(request, pet_id):

  pet = get_object_or_404(PetPost, id=pet_id)
 
  if request.user == pet.user:
    pet.delete()
    messages.success(request, "Pet deleted successfully.")
  else:
    messages.error(request, "You don't have permission to delete this pet.")
  return redirect('totalPets')