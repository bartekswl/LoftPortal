from django.shortcuts import render

def show_all(request):
    return render(request, 'parcels/show_all.html')
