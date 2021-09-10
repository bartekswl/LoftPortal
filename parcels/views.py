from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from django.contrib.admin.views.decorators import staff_member_required
from .models import Parcel



@staff_member_required(redirect_field_name=None)
def show_all(request):
   
   
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

    context = {
        'today_format': today_format,
        'today_parcels': today_parcels,
        'parcels_zip': parcels_zip,
        'total_num': total_num,
        }

    return render(request, 'parcels/show_all.html', context)



def parcel_details(request, parcel_num):

    parcel = get_object_or_404(Parcel, parcel_num=parcel_num)

    context = {
        'parcel': parcel,
    }

    return render(request, 'parcels/parcel_details.html', context)