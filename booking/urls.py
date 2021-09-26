from django.urls import path
from . import views


urlpatterns = [
    path('gym/', views.view_all_gym, name='view_all_gym'),
    
    ]