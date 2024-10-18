from django.urls import path

from adoption import views

app_name = 'adoption'

urlpatterns = [
    path('', views.index, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_details, name='pet_details')
]
