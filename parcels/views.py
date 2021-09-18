from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta, date
from django.utils.timezone import make_aware
from django.contrib.admin.views.decorators import staff_member_required
from .models import Parcel
from property.models import Concierge
from django.db.models import Q



@staff_member_required(redirect_field_name=None)
def show_all(request):
   
    if 'pickup_single' in request.POST:
        flat_number = request.POST.get('flat_number')
        parcel_num = request.POST.get('parcel_num')
        concierge = Concierge.objects.get(name=request.POST.get('concierge'))
        picked_by = request.POST.get('picked_by')
        naive_time = datetime.now()
        time_stamp = make_aware(naive_time).strftime('%Y-%m-%d %H:%M')
        Parcel.objects.filter(flat_number__flat_number=flat_number, parcel_num=parcel_num).update(
            is_collected = True,
            pickup_date = time_stamp,
            picked_up_by = picked_by,
            released_by = concierge,
        )
       
        

    picked_by = None
    collected_parcels = None
    if 'pickup_all' in request.POST:
       
      
        flat = request.POST.get('flat')
        picked_by = request.POST.get('picked_by')
        concierge = Concierge.objects.get(name=request.POST.get('concierge'))
        collected_parcels = Parcel.objects.filter(flat_number__flat_number__icontains=flat)
        naive_time = datetime.now()
        time_stamp = make_aware(naive_time).strftime('%Y-%m-%d %H:%M')
   
        for i in collected_parcels:
            Parcel.objects.filter(id=i.id).update(
                is_collected=True, 
                released_by=concierge, 
                pickup_date=time_stamp, 
                picked_up_by=picked_by
                )
            
    
    today_format = datetime.now().strftime("%d" + "/" + "%m %A")
    today_parcels = Parcel.get_today()
    rest_parcels = Parcel.group()
    all_parcels_by_day = rest_parcels[0]
    num_parcel_by_day = rest_parcels[1]
    
    parcels_zip = zip(all_parcels_by_day, num_parcel_by_day)

    if today_parcels != None:
        total_num = today_parcels[1] + sum(num_parcel_by_day)
    else:
        total_num = sum(num_parcel_by_day)

    search_lists = Parcel.find_autocomplete()
    search_list_flat = search_lists[0]
    search_list_name = search_lists[1]

    context = {
        'today_format': today_format,
        'today_parcels': today_parcels,
        'parcels_zip': parcels_zip,
        'total_num': total_num,
        'search_list_flat': search_list_flat,
        'search_list_name': search_list_name,
        'collected_parcels': collected_parcels,
        'picked_by': picked_by,
        }


    return render(request, 'parcels/show_all.html', context)

  



@staff_member_required(redirect_field_name=None)
def search_results(request):

    if 'flat' in request.GET and 'tenant_name' in request.GET:    
        results = None
        if request.GET.get('flat') == "" and request.GET.get('tenant_name') == "":
            return redirect('show_all')
        else:
            flat = request.GET.get('flat')
            tenant_name = request.GET.get('tenant_name')

            

        if tenant_name == "":
            results = Parcel.objects.filter(flat_number__flat_number__icontains=flat, is_collected=False).order_by('-date_arrived')
        
        elif flat == "":
            tenant_name = tenant_name.split()
        
            if len(tenant_name) == 2:
                results = Parcel.objects.filter(Q(tenant__name__icontains=tenant_name[0]) & Q(tenant__surname__icontains=tenant_name[1]), is_collected=False).order_by('-date_arrived')
            if len(tenant_name) == 1:
                results = Parcel.objects.filter(Q(tenant__name__icontains=tenant_name[0]) | Q(tenant__surname__icontains=tenant_name[0]), is_collected=False).order_by('-date_arrived')

        else:
            tenant_name = tenant_name.split()
            if len(tenant_name) == 2:
                results = Parcel.objects.filter(Q(flat_number__flat_number__icontains=flat) & Q(tenant__name__icontains=tenant_name[0]) & Q(tenant__surname__icontains=tenant_name[1]), is_collected=False).order_by('-date_arrived')
            if len(tenant_name) == 1:
                results = Parcel.objects.filter(Q(flat_number__flat_number__icontains=flat) & Q(tenant__name__icontains=tenant_name[0]) | Q(flat_number__flat_number__icontains=flat) & Q(tenant__surname__icontains=tenant_name[0]), is_collected=False).order_by('-date_arrived')
        tenant_name = request.GET.get('tenant_name')
        concierge_all = Concierge.objects.all()
   
    search_lists = Parcel.find_autocomplete()
    search_list_flat = search_lists[0]
    search_list_name = search_lists[1]
  
    check_results = []
    if results != None:
        list_value = None
        for i in results:
            if list_value == None:
                list_value = str(i.flat_number)
                check_results.append(True)
            elif list_value == str(i.flat_number):
                check_results.append(True)
                list_value = str(i.flat_number)
            else:
                check_results.append(False)
                list_value = str(i.flat_number)

    one_flat_in_results = all(check_results)
    
        
    context = {
        'flat': flat,
        'tenant_name': tenant_name,
        'results': results,
        'search_list_flat': search_list_flat,
        'search_list_name': search_list_name,
        'concierge_all': concierge_all,
        'one_flat_in_results': one_flat_in_results,
    }

    return render(request, 'parcels/search_results.html', context)




@staff_member_required(redirect_field_name=None)
def parcel_details(request, parcel_num):

    if request.method == "POST":
        note = request.POST.get('edit_notes')
        num = request.POST.get('num')
        updated_parcel = get_object_or_404(Parcel, parcel_num=num)
        updated_parcel.additional_notes = note
        updated_parcel.save()
        
    parcel = get_object_or_404(Parcel, parcel_num=parcel_num)
    days_in = (make_aware(datetime.now())-parcel.date_arrived).days
    concierge_all = Concierge.objects.all()
   

    context = {
        'parcel': parcel,
        'days_in': days_in,
        'concierge_all': concierge_all,
    }

    return render(request, 'parcels/parcel_details.html', context)


# SCRIPT FOR SEARCH ALL PARCELS- EVEN PICKED UP
#    if 'flat' in request.GET and 'tenant_name' in request.GET:    
#         results = None
#         if request.GET.get('flat') == "" and request.GET.get('tenant_name') == "":
#             return redirect('show_all')
#         else:
#             flat = request.GET.get('flat')
#             tenant_name = request.GET.get('tenant_name')

            

#         if tenant_name == "":
#             results = Parcel.objects.filter(flat_number__flat_number__icontains=flat).order_by('-date_arrived')
        
#         elif flat == "":
#             tenant_name = tenant_name.split()
        
#             if len(tenant_name) == 2:
#                 results = Parcel.objects.filter(Q(tenant__name__icontains=tenant_name[0]) & Q(tenant__surname__icontains=tenant_name[1])).order_by('-date_arrived')
#             if len(tenant_name) == 1:
#                 results = Parcel.objects.filter(Q(tenant__name__icontains=tenant_name[0]) | Q(tenant__surname__icontains=tenant_name[0])).order_by('-date_arrived')

#         else:
#             tenant_name = tenant_name.split()
#             if len(tenant_name) == 2:
#                 results = Parcel.objects.filter(Q(flat_number__flat_number__icontains=flat) & Q(tenant__name__icontains=tenant_name[0]) | Q(flat_number__flat_number__icontains=flat) & Q(tenant__surname__icontains=tenant_name[1])).order_by('-date_arrived')
#             if len(tenant_name) == 1:
#                 results = Parcel.objects.filter(Q(flat_number__flat_number__icontains=flat) & Q(tenant__name__icontains=tenant_name[0]) | Q(flat_number__flat_number__icontains=flat) & Q(tenant__surname__icontains=tenant_name[0])).order_by('-date_arrived')
#         tenant_name = request.GET.get('tenant_name')
#         concierge_all = Concierge.objects.all()
   
#     search_lists = Parcel.find_autocomplete()
#     search_list_flat = search_lists[0]
#     search_list_name = search_lists[1]