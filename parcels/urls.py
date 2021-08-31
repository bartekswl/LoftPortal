from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_all, name='show_all'),
]