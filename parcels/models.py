from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from property.models import Flat, Tenant, Concierge
from datetime import datetime, timedelta, date
from django.core.validators import MinValueValidator, MaxValueValidator

from random import randint



def parcel_num_generator():
        new_num = 'SE'+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))
        return new_num

class Parcel(models.Model):

    date_arrived     = models.DateTimeField(auto_now_add=True, null=True)
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
        check_flat = Flat.get_tenants(self.flat_number)[0]
        if self.tenant:
            if not self.tenant in check_flat:    
                raise ValidationError(_('Flat number does not match tenant name.'))

    def __str__(self):
        return str(self.date_arrived.date())