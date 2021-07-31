from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime

from property.models import Flat, Tenant, Concierge

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect





gym_time_slots = (('6', '6'),('7', '7'), ('8', '8'), ('9', '9'),('xxx', 'xxx'), ('11', '11'), 
    ('12', '12'), ('13', '13'),('14', '14'), ('15', '15'), ('16', '16'),('17', '17'), ('18', '18'),
    ('19', '19'),('20', '20'), ('21', '21'))

def validate_date(date):
    if date < datetime.datetime.now().date():
        raise ValidationError("Date cannot be in the past")



class GymBooking(models.Model):

    date          = models.DateField(auto_now_add=False, null=True, blank=False, validators=[validate_date])
    time          = models.CharField(max_length=3, choices=gym_time_slots, null=True, blank=False)
    flat          = models.ForeignKey(Flat, on_delete=models.PROTECT, null=True, blank=False)
    pax           = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], null=True, blank=False, default=1)
    tenant        = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=False)
    made_by       = models.ForeignKey(Concierge, on_delete=models.SET_NULL, null=True, blank=False)
    date_added    = models.DateTimeField(auto_now_add=True, null=True)
    no_show       = models.BooleanField(default=False)
    
 
        
  
    
    def clean(self):
        
        check_flat = Flat.get_tenants(self.flat)[0]
        if self.time == 'xxx': # Cleaning slot chosen- not available
            raise ValidationError(_('Time slot not available- cleaning'))
        # Checking if tenant matches the flat number
        if not self.tenant in check_flat:    
            raise ValidationError(_('Flat number does not match tenant name.'))
        # checking for blocked/full slots
        if self.check_blocks():
            raise ValidationError(_('Chosen slot is blocked by admin'))
        if self.check_avail():
            raise ValidationError(_('Slot is full'))
       

       
        # Algorithm going through blocked slots- checking for day/hourly and returning permission/rejection to book
    def check_blocks(self):
        if GymBookingBlock.objects.filter(date=self.date).exists():
            if GymBookingBlock.objects.filter(date=self.date, all_day=True).exists():
                return True

            else:
                all_blocks = GymBookingBlock.objects.filter(date=self.date)
                loop_outcome = []
                booking_time = int(self.time)

                try:
                    dur_query = int(self.duration)
                except:
                    pass
                
                for block in all_blocks:
                    block_time = int(block.time)
                    block_duration = int(block.duration)
                    if booking_time == block_time:
                        loop_outcome.append(0)
                    if booking_time < block_time:
                        if dur_query:
                            if booking_time + dur_query <= block_time:
                                loop_outcome.append(1)
                            elif booking_time + dur_query > block_time:
                                loop_outcome.append(0)
                        loop_outcome.append(1)
                    if booking_time > block_time:
                        release_time = block_time + block_duration
                        if booking_time >= release_time:
                            loop_outcome.append(1)
                        else:
                            loop_outcome.append(0)
                if 0 in loop_outcome:
                    return True

                else:
                    return False


           
            # Checks how many bookings exists already- max 6 per hour (or 6 people)
    def check_avail(self):
        existing_bookings = GymBooking.objects.filter(date=self.date, time=self.time)
        numof_bookings = existing_bookings.count()
        slot_pax = []

        if not self.pk:
            for booking in existing_bookings:
                slot_pax.append(booking.pax)
        
            if numof_bookings >= 6:
                return True
            if sum(slot_pax) + self.pax > 6:
                return True

        else:
            for booking in existing_bookings:
                if booking.pk == self.pk:
                    pass
                else:
                    slot_pax.append(booking.pax)
         
            if sum(slot_pax) + self.pax > 6:
                return True

        

      
        
     
      
    def __str__(self):
        return str(f'{self.flat} {self.tenant}')








gym_block_slots = (('1', '1'),('2', '2'), ('3', '3'), ('4', '4'),('5', '5'), ('6', '6'), 
    ('7', '7'), ('8', '8'),('9', '9'), ('10', '10'), ('11', '11'),('12', '12'), ('13', '13'),
    ('14', '14'),('15', '15'))


class GymBookingBlock(models.Model):

    date          = models.DateField(auto_now_add=False, null=True, blank=False, validators=[validate_date])
    all_day       = models.BooleanField(default=False)
    time          = models.CharField(max_length=3, choices=gym_time_slots, null=True, blank=True)
    duration      = models.CharField(max_length=2, choices=gym_block_slots, null=True, blank=True)
    block_by      = models.ForeignKey(Concierge, on_delete=models.SET_NULL, null=True, blank=False)


    def clean(self):
        if self.all_day == True:
            if self.time != None or self.duration != None:
                raise ValidationError(_("Don't input time or duration for all day block."))
        else:
            if self.time == None or self.duration == None:
                raise ValidationError(_("Please specify time and duration of block"))
        if GymBooking.check_blocks(self):
            raise ValidationError(_("Block already exists"))



    def __str__(self):
        return str(self.date)