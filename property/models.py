from django.db import models
from model_utils import FieldTracker
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from django.contrib import messages
from datetime import datetime, timedelta, date

from property.flat_codes import flat_codes
from accounts.models import PortalUser

from random import randint

# from django.core.exceptions import ValidationError

#validators=[validate_even]
# def validate_even(value):
#     if value != 'Cassia':
        # raise ValidationError(
        #     _('%(value)s is not an even number'),
        #     params={'value': value},
        # )


def validate_date(date):
    if date > datetime.now().date():
        raise ValidationError("Date cannot be in the future")

building_codes = (('Cassia', 'Cassia'),('Rosewood', 'Rosewood'))
own_flat_type = (('Vonder', 'Vonder'),('Anglo', 'Anglo'), ('Private', 'Private'), ('Other', 'Other'))

class Flat(models.Model):
    
    flat_number    = models.CharField(max_length=4, choices=flat_codes, null=True, blank=False, unique=True)
    building       = models.CharField(max_length=8, choices=building_codes, null=True, blank=False)
    core           = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=False)
    floor          = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], null=True, blank=False)
    flat_size      = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True, blank=False)
    electric_meter = models.CharField(max_length=12, null=True, blank=True, unique=True)
    last_reading_date = models.DateField(auto_now_add=False, null=True, blank=True, validators=[validate_date])
    last_reading   = models.CharField(max_length=10, null=True, blank=True)
    water_meter    = models.CharField(max_length=12, null=True, blank=True, unique=True)
    heat_meter     = models.CharField(max_length=12, null=True, blank=True, unique=True)
    full_address   = models.CharField(max_length=40, null=True, blank=True)
    flat_type      = models.CharField(max_length=10, choices=own_flat_type, null=True, blank=False)
    agency         = models.CharField(max_length=20, null=True, blank=True)
    agency_contact = models.CharField(max_length=50, null=True, blank=True)
    auth_access    = models.CharField(max_length=100, blank=True)
    additional_notes= models.TextField(max_length=300, blank=True)
    is_empty       = models.BooleanField(default=False)
    
    
    
    
    def clean(self):
        if self.flat_number.startswith('C') and self.building != 'Cassia':
            raise ValidationError(_('Flats starting with C can only belong to Cassia Building'))

    def get_tenants(self):
        flat_tenants = Tenant.objects.filter(flat=self, moved_out=False)
        how_many = flat_tenants.count()
        return [flat_tenants, how_many]

    # def numof_tenants(self):
    #     flat_tenants = Tenant.objects.filter(flat=self)
    #     how_many = flat_tenants.count()
    #     return flat_tenants
    
    

    def __str__(self):
        return self.flat_number





def pin_generator():
    new_pin ='se'+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))
    return new_pin

tenancy = (('Tenant', 'Tenant'),('Owner', 'Owner'), ('Other', 'Other'))

class Tenant(models.Model):

    name          = models.CharField(max_length=15, null=True, blank=False)
    surname       = models.CharField(max_length=30, null=True, blank=False)
    email         = models.EmailField(max_length=50, unique=True)
    phone_number  = models.CharField(max_length=20, null=True, blank=True, unique=True)
    flat          = models.ForeignKey(Flat, on_delete=models.PROTECT)
    status        = models.CharField(max_length=10, choices=tenancy, null=True, blank=False)
    stay_length   = models.CharField(max_length=20, null=True, blank=False)
    pet_licence   = models.CharField(max_length=20, null=True, blank=False)
    additional_notes= models.TextField(max_length=300, blank=True)
    date_moved_in = models.DateField(auto_now_add=False, null=True, blank=True)
    date_added    = models.DateField(auto_now_add=True, null=True)
    moved_out     = models.BooleanField(default=False)
    date_moved_out= models.DateField(auto_now_add=False, null=True, blank=True)
    pin_code      = models.CharField(max_length=6, default=pin_generator, editable=False)
    portal_user   = models.OneToOneField(PortalUser, related_name='tenant', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    tracker_agent = FieldTracker(fields=['flat', 'moved_out'])
    




    class Meta:
        unique_together = ('name', 'surname',)

    def clean(self):
        if not self.pk:
            amount_tenants = Flat.get_tenants(self.flat)[1]
            if amount_tenants >= 6:
                raise ValidationError(_('Maximum flat occupancy is 6. Mark all former tenants as "moved out" '))
        elif amount_tenants > 6:
            raise ValidationError(_('Maximum flat occupancy is 6. Mark all former tenants as "moved out" '))
        else:
            if self.tracker_agent.has_changed('flat') or self.tracker_agent.has_changed('moved_out'):
                if amount_tenants >= 6:
                    raise ValidationError(_('Maximum flat occupancy is 6.'))
            
   
    def create_user(self):
        if not self.portal_user:
            user = PortalUser.objects.create_user(
                name=self.name,
                surname=self.surname,
                email=self.email,
                phone_number=self.phone_number,
                flat=self.flat.flat_number,
                )
            self.portal_user = user
            self.save()
     

    def save(self, *args, **kwargs):
       
        if self.portal_user:
             self.portal_user.name = self.name
             self.portal_user.surname = self.surname
             self.portal_user.phone_number = self.phone_number
             flat_to_string = str(self.flat)
             self.portal_user.flat = flat_to_string
             self.portal_user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}' 





class CommercialUnit(models.Model):

    unit_number        = models.CharField(max_length=5, null=True, blank=False, unique=True)
    business_name      = models.CharField(max_length=20, null=True, blank=False)
    street_location    = models.CharField(max_length=20, null=True, blank=False)
    full_address       = models.CharField(max_length=40, null=True, blank=True)
    contact_name       = models.CharField(max_length=30, null=True, blank=True)
    contact_email      = models.EmailField(max_length=50, null=True, blank=True, unique=True)
    contact_number     = models.CharField(max_length=20, null=True, blank=True, unique=True)
    is_running         = models.BooleanField(default=False)


    def __str__(self):
        return self.unit_number






work_choices = (('Day', 'Day'),('Night', 'Night'), ('Other', 'Other'))

class Concierge(models.Model):

    name            = models.CharField(max_length=15, null=True, blank=False, unique=True)
    surname         = models.CharField(max_length=15, null=True, blank=True)
    email           = models.EmailField(max_length=50, unique=True, null=True, blank=True)
    work_pattern    = models.CharField(max_length=6, choices=work_choices, null=True, blank=False)
    phone_number    = models.CharField(max_length=20, null=True, blank=True, unique=True)

    

    def __str__(self):
        return self.name




class Complaint(models.Model):

    date        = models.DateField(auto_now_add=False, null=True, blank=False, validators=[validate_date])
    flat        = models.ForeignKey(Flat, on_delete=models.PROTECT, related_name='complainee', null=True, blank=False)
    placed_by   = models.ForeignKey(Flat, on_delete=models.PROTECT, related_name='complainant', null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=False)
    logged_by   = models.ForeignKey(Concierge, on_delete=models.PROTECT, null=True, blank=False)


    def __str__(self):
        return f'{self.date} {self.flat}' 