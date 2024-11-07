from django.contrib.auth.models import AbstractUser
from django.db import models
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

  # Set the username field
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
      return self.username

class PetPost(models.Model):
  user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='pet_posts')
  title = models.CharField(max_length=100)
  image = models.ImageField(upload_to='uploads/', blank=False, null=False)
  pet_type = models.CharField(max_length=50, blank=False, null=False)
  gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
  description = models.TextField(blank=False, null=False)
  location = models.CharField(max_length=100, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.title
