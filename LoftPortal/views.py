from django.shortcuts import render, get_object_or_404
from property.models import Tenant, Flat
from accounts.models import PortalUser



def home(request):
    # current_tenant = get_object_or_404(Tenant, name='Bar')
    # Tenant.create_user(current_tenant)
    # a =  get_object_or_404(Flat, flat_number='C1')
    # b = Flat.get_tenants(a)
    # print(b[0])
    # print(b[1])
    # a = get_object_or_404(Tenant, pk=11)
    PortalUser.objects.create_admin('Benek','gruby@op.pl')
    return render(request, 'home.html')