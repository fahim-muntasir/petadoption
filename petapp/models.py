from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import os
# from django.contrib.auth import get_user_model

# User = get_user_model()

class UserProfile(AbstractUser):
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  phone_number = models.CharField(max_length=15)
  additional_number = models.CharField(max_length=15, blank=True, null=True)
  address = models.TextField()
  state = models.CharField(max_length=100)
  social_media_link = models.URLField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
  
  # Set the username field
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
      return self.username

# class PetPost(models.Model):
#   user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='pet_posts')
#   title = models.CharField(max_length=100)
#   image = models.ImageField(upload_to='uploads/', blank=False, null=False)
#   pet_type = models.CharField(max_length=50, blank=False, null=False)
#   gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
#   description = models.TextField(blank=False, null=False)
#   age = models.CharField(max_length=50, blank=False, null=True)
#   status = models.CharField(
#     max_length=10,
#     choices=[('Active', 'Active'), ('Adopted', 'Adopted')],
#     default='Active',
#   )
#   division = models.CharField(max_length=50, blank=False,null=True)
#   district = models.CharField(max_length=50, blank=False, null=True)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

#   def __str__(self):
#       return self.title

class PetPost(models.Model):
  user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='pet_posts')
  title = models.CharField(max_length=100)
  image = models.ImageField(upload_to='uploads/', blank=False, null=False)
  pet_type = models.CharField(max_length=50, blank=False, null=False)
  gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
  description = models.TextField(blank=False, null=False)
  age = models.CharField(max_length=50, blank=False, null=True)
  status = models.CharField(
      max_length=10,
      choices=[('Active', 'Active'), ('Adopted', 'Adopted')],
      default='Active',
  )
  division = models.CharField(max_length=50, blank=False, null=True)
  district = models.CharField(max_length=50, blank=False, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)  # Save the original image first
    if self.image:
      img = Image.open(self.image.path)
      
      # Step 1: Resize to a maximum dimension
      max_size = (1024, 1024)  # Adjust this as needed
      img.thumbnail(max_size)  # Maintain aspect ratio

      # Step 2: Save the image with reduced quality to meet 4MB limit
      file_path = self.image.path
      img.save(file_path, optimize=True, quality=85)

      # Step 3: Ensure the file is under 4MB by reducing quality iteratively
      while os.path.getsize(file_path) > 4 * 1024 * 1024:  # Check file size
        img.save(file_path, optimize=True, quality=75)  # Reduce quality further

  def __str__(self):
      return self.title

class Message(models.Model):
    sender = models.ForeignKey('UserProfile', related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey('UserProfile', related_name="received_messages", on_delete=models.CASCADE)
    pet_post = models.ForeignKey(PetPost, on_delete=models.CASCADE, blank=True,null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

