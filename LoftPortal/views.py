from django.shortcuts import render, get_object_or_404
from property.models import Tenant



def home(request):
    current_tenant = get_object_or_404(Tenant, name='Bar')
    Tenant.create_user(current_tenant)
    return render(request, 'home.html')