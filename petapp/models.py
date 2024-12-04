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
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
  
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
  age = models.CharField(max_length=50, blank=False, null=True)
  status = models.CharField(
    max_length=10,
    choices=[('Active', 'Active'), ('Adopted', 'Adopted')],
    default='Active',
  )
  division = models.CharField(max_length=50, blank=False,null=True)
  district = models.CharField(max_length=50, blank=False, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

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

