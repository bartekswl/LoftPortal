from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta, date
from django.utils.timezone import make_aware
from django.contrib.admin.views.decorators import staff_member_required

from .models import GymBooking, GymBookingBlock
from property.models import Concierge, Flat, Tenant

from django.contrib import messages
from django.db.models import Q




@staff_member_required(login_url ='login')
def view_all_gym(request):



    days_dates = []
    today_date = make_aware(datetime.now()).date()
    for i in range(1,8):
        booking_hourly = {}
        if i == 1:
            day_date = today_date
            days_dates.append(day_date)
        else:
            day_date += timedelta(days=1)
            days_dates.append(day_date)
        day_booking = GymBooking.objects.filter(date=day_date)
        for x in range(6,22):
            if day_booking.filter(time=x):
                booking_hourly[x] = day_booking.filter(time=x)
            else:
                booking_hourly[x] = None
            
            globals()[f"daily{i}"] = booking_hourly
    
    seven_days_bookings = {
        'one': daily1,
        'two': daily2,
        'three': daily3,
        'four': daily4,
        'five': daily5,
        'six': daily6,
        'seven': daily7,
    }

    elements_zip = zip(seven_days_bookings.items(), days_dates)




    context = {
        'seven_days_bookings': seven_days_bookings,
        'elements_zip': elements_zip,

    }

    return render(request, 'booking/gym/view_all_gym.html', context)




