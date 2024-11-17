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
  path('dashboard/',views.dashboard, name='dashboard'),
  path('totalRequest/',views.totalRequest, name='totalRequest'),
  path('updateInfo/',views.updateInfo, name='updateInfo'),
  path('userprofile/<int:userid>',views.userProfile, name='userprofile'),
  path('totalPets/',views.totalPets, name='totalPets'),
  path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
  path('delete_pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),
  path('update_pet/<int:pet_id>/', views.updatePet, name='updatePet'),
  path('get-districts/', views.get_districts, name='get-districts'),
]