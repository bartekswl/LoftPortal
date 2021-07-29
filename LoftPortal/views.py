from django.shortcuts import render, get_object_or_404
from property.models import Tenant, Flat



def home(request):
    # current_tenant = get_object_or_404(Tenant, name='Bar')
    # Tenant.create_user(current_tenant)
    # a =  get_object_or_404(Flat, flat_number='C1')
    # b = Flat.get_tenants(a)
    # print(b[0])
    # print(b[1])
    return render(request, 'home.html')