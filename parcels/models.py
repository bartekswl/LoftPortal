from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from property.models import Flat, Tenant, Concierge
from datetime import datetime, timedelta, date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import make_aware
from random import randint

from django.db.models import Sum





def parcel_num_generator():
        
        month = str(datetime.now().date().month)
        if len(month) == 1:
            month = '0' + month
        day = str(datetime.now().date().day)
        if len(day) == 1:
            day = '0' + day
        new_num = 'SE'+ day + month + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
        return new_num


class Parcel(models.Model):

    date_arrived     = models.DateTimeField(null=True, blank=True)
    flat_number      = models.ForeignKey(Flat, on_delete=models.PROTECT, null=True, blank=False)
    tenant           = models.ForeignKey(Tenant, on_delete=models.PROTECT, null=True, blank=True)
    amount_parcels   = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], null=True, blank=False, default=1)
    received_by      = models.ForeignKey(Concierge, on_delete=models.PROTECT, null=True, blank=False)
    parcel_num       = models.CharField(max_length=8, default=parcel_num_generator, editable=False)
    is_collected     = models.BooleanField(default=False)
    pickup_date      = models.DateTimeField(auto_now=False, null=True, blank=True)
    picked_up_by     = models.CharField(max_length=20, null=True, blank=True)
    released_by      = models.ForeignKey(Concierge, on_delete=models.PROTECT, null=True, blank=True, related_name='released')
    additional_notes = models.TextField(max_length=100, blank=True)

   

    def clean(self):
        if not self.pk:
            naive_time = datetime.now()
            self.date_arrived = make_aware(naive_time).strftime('%Y-%m-%d %H:%M')
        check_flat = Flat.get_tenants(self.flat_number)[0]
        if self.tenant:
            if not self.tenant in check_flat:    
                raise ValidationError(_('Flat number does not match tenant name.'))


    def get_today():
        today_parcels = Parcel.objects.filter(date_arrived__date=datetime.now().date()).order_by('-date_arrived')
        if len(today_parcels) == 0:
            return None
        else:
            num_of_parcels = today_parcels.aggregate(sum=Sum('amount_parcels'))
            return today_parcels, num_of_parcels['sum']

    def all_but_today():
        all_but_today = Parcel.objects.exclude(date_arrived__date=datetime.now().date()).all().order_by('-date_arrived')
        return all_but_today

    def format_time(self):
        day_header = self.date_arrived.strftime("%d" + "/" + "%m %A")
        return day_header

    def group():
        all_parcels = Parcel.all_but_today()
        a=0
        final_list  = []
        same_date = []
        date = None
        num_of_parcels = {}
        parcels = []

        for i in all_parcels:
            if a == 0:
                same_date.append(i)
                date = i.date_arrived.date()
                parcels.append(i.amount_parcels)
                
            if i.date_arrived.date() == date and a != 0:
                same_date.append(i)
                date = i.date_arrived.date()
                parcels.append(i.amount_parcels)

            if i.date_arrived.date() != date and date != None:
                final_list.append(same_date)
                num_temp = sum(parcels)
                num_of_parcels[date] = (num_temp)
                parcels = []
                same_date = []
                same_date.append(i)
                parcels.append(i.amount_parcels)
                date = i.date_arrived.date()
            
            a = a + 1
        
        if len(same_date) > 0:
            final_list.append(same_date)
            num_temp = sum(parcels)
            num_of_parcels[date] = (num_temp)
        
        num_of_parcels_ready = []
        for i in num_of_parcels.values():
            num_of_parcels_ready.append(i)
     
        return final_list, num_of_parcels_ready

            
            
          

    
    def __str__(self):
        return str(self.date_arrived)