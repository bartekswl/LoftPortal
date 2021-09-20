from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_all, name='show_all'),
    path('search_results/', views.search_results, name='search_results'),
    path('new_parcel/', views.new_parcel, name='new_parcel'),
    path('<slug:parcel_num>/', views.parcel_details, name='parcel_details'),
    
    ]