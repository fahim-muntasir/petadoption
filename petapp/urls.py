from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('login/', views.user_login, name='login'),
  path('logout/', views.user_logout, name='logout'),
  path('registration/', views.registration, name='registration'),
  path('about/', views.about, name='about'),
  path('items/', views.items, name='items'),
  path('item/<int:id>/', views.item, name='item'),
  path('createPet/', views.createPet, name='createPet'),
  # path('modal/', views.modal, name='modal'),
  path('dashboard/',views.dashboard, name='dashboard'),
  path('totalRequest/',views.totalRequest, name='totalRequest'),
  path('updateInfo/',views.updateInfo, name='updateInfo'),
  path('totalPets/',views.totalPets, name='totalPets'),
]