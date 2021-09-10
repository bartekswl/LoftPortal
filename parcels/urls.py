from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_all, name='show_all'),
    path('<slug:parcel_num>/', views.parcel_details, name='parcel_details'),
]