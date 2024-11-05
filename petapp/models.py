from django.contrib.auth.models import AbstractUser
from django.db import models

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
