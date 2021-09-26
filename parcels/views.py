from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta, date
from django.utils.timezone import make_aware
from django.contrib.admin.views.decorators import staff_member_required
from .models import Parcel
from property.models import Concierge, Flat, Tenant
from django.db.models import Q
from django.contrib import messages





@staff_member_required(login_url ='login')
def show_all(request):

    
    if 'parcel_del_btn' in request.POST:
        obj = Parcel.objects.filter(parcel_num=request.POST.get('parcel_del'))
        obj_age = make_aware(datetime.now()) - obj[0].date_arrived
        if obj_age.days < 32:
            messages.error(request, " You can't remove records for at least 1 month from the date of creation.")
        else:
            obj.delete()
            messages.success(request, ' Delivery removed from database.')

   
    picked_by = None
    collected_parcels = None
    if 'pickup_single' in request.POST:
        flat_number = request.POST.get('flat_number')
        parcel_num = request.POST.get('parcel_num')
        concierge = Concierge.objects.get(name=request.POST.get('concierge'))
        picked_by = request.POST.get('picked_by')
        naive_time = datetime.now()
        time_stamp = make_aware(naive_time)
        collected_parcels = Parcel.objects.filter(flat_number__flat_number=flat_number, parcel_num=parcel_num)
        
        collected_parcels.update(
            is_collected = True,
            pickup_date = time_stamp,
            picked_up_by = picked_by,
            released_by = concierge,
            turnover = Parcel.get_turnover(collected_parcels[0])
        )
       
        

    
    if 'pickup_all' in request.POST:
       
      
        flat = request.POST.get('flat')
        tenant = request.POST.get('tenant').split()
        picked_by = request.POST.get('picked_by')
        concierge = Concierge.objects.get(name=request.POST.get('concierge'))
        if len(tenant) > 0:
            collected_parcels = Parcel.objects.filter(Q(tenant__name__icontains=tenant[0]) | Q(tenant__surname__icontains=tenant[0]), flat_number__flat_number__icontains=flat, is_collected=False).order_by('-date_arrived')
        else:
            collected_parcels = Parcel.objects.filter(flat_number__flat_number__icontains=flat, is_collected=False).order_by('-date_arrived')
        naive_time = datetime.now()
        time_stamp = make_aware(naive_time)
   
        for i in collected_parcels:
            Parcel.objects.filter(id=i.id).update(
                is_collected=True, 
                released_by=concierge, 
                pickup_date=time_stamp, 
                picked_up_by=picked_by,
                turnover = Parcel.get_turnover(i)
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

    results = None
    flat = None
    tenant_name = None
    concierge_all = None
    if 'flat' in request.GET and 'tenant_name' in request.GET:    
        
        if request.GET.get('flat') == "" and request.GET.get('tenant_name') == "":
            return redirect('show_all')
        else:
            flat = request.GET.get('flat')
            tenant_name = request.GET.get('tenant_name')

            

        if tenant_name == "":
            results = Parcel.objects.filter(flat_number__flat_number__icontains=flat, is_collected=False).order_by('-date_arrived')
        
        elif flat == "":
            tenant_name = tenant_name.split()

            if len(tenant_name) > 2:
                results = None
            if len(tenant_name) == 2:
                results = Parcel.objects.filter(Q(tenant__name__icontains=tenant_name[0]) & Q(tenant__surname__icontains=tenant_name[1]), is_collected=False).order_by('-date_arrived')
            if len(tenant_name) == 1:
                results = Parcel.objects.filter(Q(tenant__name__icontains=tenant_name[0]) | Q(tenant__surname__icontains=tenant_name[0]), is_collected=False).order_by('-date_arrived')

        else:
            tenant_name = tenant_name.split()
            if len(tenant_name) > 2:
                results = None
            if len(tenant_name) == 2:
                results = Parcel.objects.filter(Q(flat_number__flat_number__icontains=flat) & Q(tenant__name__icontains=tenant_name[0]) & Q(tenant__surname__icontains=tenant_name[1]), is_collected=False).order_by('-date_arrived')
            if len(tenant_name) == 1:
                results = Parcel.objects.filter(Q(flat_number__flat_number__icontains=flat) & Q(tenant__name__icontains=tenant_name[0]) | Q(flat_number__flat_number__icontains=flat) & Q(tenant__surname__icontains=tenant_name[0]), is_collected=False).order_by('-date_arrived')
        tenant_name = request.GET.get('tenant_name')
        concierge_all = Concierge.objects.only('name')
   
    search_lists = Parcel.find_autocomplete()
    search_list_flat = search_lists[0]
    search_list_name = search_lists[1]
  
    # Checks if there is one flat appearing in results; if yes= collect all parcels button enabled #
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


    if 'edit_notes_btn' in request.POST:
        note = request.POST.get('edit_notes')
        print(note)
        num = request.POST.get('num')
        print(num)
        updated_parcel = get_object_or_404(Parcel, parcel_num=num)
        updated_parcel.additional_notes = note
        updated_parcel.save()
        messages.success(request, ' Notes for this parcel were updated.')
        
    parcel = get_object_or_404(Parcel, parcel_num=parcel_num)
    days_in = Parcel.get_turnover(parcel)
    concierge_all = Concierge.objects.only('name')
   

    context = {
        'parcel': parcel,
        'days_in': days_in,
        'concierge_all': concierge_all,
    }

    return render(request, 'parcels/parcel_details.html', context)



@staff_member_required(redirect_field_name=None)
def new_parcel(request):
   
    flat_codes = None
    amount_parcels_list = None
    concierge_all = None
    concierge = None
    tenants_list = None

    form_invalid = False

    if 'new_parcels' in request.POST:
        # Creating new Parcel objects when input is valid and tenants match the flat #
        try:
            added_success = None
            for i in range(1, int(request.POST.get('amount_deliveries'))+1):
                
                quantity = int(request.POST.get('quantity'+str(i)))
                concierge = Concierge.objects.get(name=request.POST.get('concierge'))

                flat = request.POST.get('flat'+str(i)).replace(' ', '')
                try:
                    flat_number = Flat.objects.get(flat_number__icontains=flat)
                except:
                    messages.error(request, " Given flat number is invalid.")
                    raise ValueError

                tenant = request.POST.get('tenant_name'+str(i))
                if 'not'.casefold() and 'found'.casefold() in tenant.casefold():
                    tenant_obj = None
                else:
                    tenant = tenant.split()
                    if len(tenant) > 2:
                        messages.error(request, " Resident's details can contain 2 words only: name and surname.")
                        raise ValueError
                    try:
                        if len(tenant) == 2:
                            tenant_obj = Tenant.objects.get(Q(name__icontains=tenant[0]) & Q(surname__icontains=tenant[1]) | Q(name__icontains=tenant[1]) & Q(surname__icontains=tenant[0]))
                        if len(tenant) == 1:
                            tenant_obj = Tenant.objects.filter(Q(name__icontains=tenant[0]) | Q(surname__icontains=tenant[0]), flat=flat_number)
                            if len(tenant_obj) > 1:
                                messages.error(request, " More than 1 matching resident- please use name and surname.")
                                raise ValueError
                            tenant_obj = tenant_obj[0]
                    except:
                        if not messages.get_messages(request):
                            messages.error(request, " Resident and flat match not found- check details or use 'NOT FOUND'")
                            raise ValueError
                    
                
                new_parcel_instance = Parcel(
                    flat_number=flat_number, 
                    tenant=tenant_obj, 
                    amount_parcels=quantity,                       ### Add email module ###
                    received_by= concierge,
                    )
                new_parcel_instance.clean()
                new_parcel_instance.save()
                added_success = i
            messages.success(request, ' New parcels added to database.')
            return redirect('show_all')
        # Returning form with input values so data can be checked by user for mistake #
        # Picking up list from moment of failed attempt #
        except:
            if added_success != None:
                failed_attempt = added_success + 1
            else:
                failed_attempt = 1
            form_invalid = True
            amount_parcels_list =[] # Keeping the same var name to avoid changing 'for loops' in template # 
            for i in range(failed_attempt,int(request.POST.get('amount_deliveries'))+1):
                iteration = []
                
                iteration.append(request.POST.get('flat'+str(i)))
                iteration.append(request.POST.get('tenant_name'+str(i)))
                iteration.append(request.POST.get('quantity'+str(i)))
                amount_parcels_list.append(iteration)
            if not messages.get_messages(request):
                messages.error(request, " Given details incorrect! Check if flat number matches resident's details; if resident name incorrect use 'NOT FOUND'")


    
    if 'amount_parcels' in request.GET:
        amount_parcels_list = list(range(1,int(request.GET.get('amount_parcels')) + 1))
        
    tenants_list = Parcel.tenants_autocomplete()
    concierge_all = Concierge.objects.only('name')
    from property.flat_codes import flat_codes
    
    context = {
        'amount_parcels_list': amount_parcels_list,
        'concierge_all': concierge_all,
        'flat_codes': flat_codes,
        'tenants_list': tenants_list,
        'concierge': concierge,
    }
        
    return render(request, 'parcels/new_parcel.html', context)



@staff_member_required(redirect_field_name=None)
def advanced_search(request):

    latest_parcel = Parcel.objects.latest('-date_arrived').date_arrived
    from property.flat_codes import flat_codes

    context = {
        'flat_codes': flat_codes,
        'latest_parcel': latest_parcel,
    }

    return render(request, 'parcels/advanced_search.html', context)




@staff_member_required(redirect_field_name=None)
def adv_search_results(request):
    
    results = None
    if 'adv_search_btn' in request.POST:
        try:
            delivery_status = request.POST.get('delivery_status')
            
            flat = request.POST.get('flat').replace(' ', '')
            if not Flat.objects.filter(flat_number__icontains=flat).exists():
                messages.error(request, " Flat number incorrect")
                raise ValueError

            tenant = request.POST.get('tenant_name').split() 
            if len(tenant) > 2:
                messages.error(request, " Resident's details can contain 2 words only: name and/or surname.")
                raise ValueError

            parcel_num = request.POST.get('parcel_num')
            if parcel_num is not "":
                if not parcel_num.casefold().startswith('se'.casefold()):
                    messages.error(request, " Parcel ID number incorrect")
                    raise ValueError

            date_arrived = request.POST.get('date_arrived')
            date_collected = request.POST.get('date_collected')

            if delivery_status == 'all':
                results = Parcel.objects.all().order_by('-date_arrived')
            elif delivery_status == 'collected':
                results = Parcel.objects.filter(is_collected=True).order_by('-date_arrived')
            elif delivery_status == 'not_collected':
                results = Parcel.objects.filter(is_collected=False).order_by('-date_arrived')
            
            if flat is not '':
                results = results.filter(flat_number__flat_number__icontains=flat)  
        
            if tenant is not []:
                if len(tenant) == 2:
                    results = results.filter(Q(tenant__name__icontains=tenant[0]) & Q(tenant__surname__icontains=tenant[1]) | Q(tenant__name__icontains=tenant[1]) & Q(tenant__surname__icontains=tenant[0]))
                if len(tenant) == 1:
                    results = results.filter(Q(tenant__name__icontains=tenant[0]) | Q(tenant__surname__icontains=tenant[0]))
            
            if parcel_num is not '':
                results = results.filter(parcel_num=parcel_num)

            if date_arrived is not None:
                results = results.filter(date_arrived__date=date_arrived)

            if date_collected is not None:
                results = results.filter(pickup_date__date=date_collected)

            from django.db.models import Sum
            total_quantity = results.aggregate(Sum('amount_parcels'))['amount_parcels__sum']
            
      
        except:            
            if not messages.get_messages(request):
                messages.error(request, " Your query was invalid- try again.")
            return redirect('advanced_search')
            

    context = {
        'results': results,
        'total_quantity': total_quantity,
    }

    return render(request, 'parcels/adv_search_results.html', context)



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