from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('login/', views.login, name='login'),
  path('registration/', views.registration, name='registration'),
  path('about/', views.about, name='about'),
  path('items/', views.items, name='items'),
  path('item/', views.item, name='item'),
  path('createPet/', views.createPet, name='createPet'),
]