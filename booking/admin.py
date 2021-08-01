from django.contrib import admin
from .models import GymBooking, GymBookingBlock, CinemaBooking, CinemaBookingBlock
from property.models import Flat, Tenant



class GymBookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'flat', 'tenant', 'pax')

    # def save_model(self,*args, **kwargs):
        
            
    #     check_flat = Flat.get_tenants(self.flat)
    #     if not self.tenant in check_flat:
    #         messages.add_message(request, messages.INFO, 'Car has been sold')
    #     else:
    #         super().save(*args, **kwargs)


        # if 'owner' in form.changed_data:
        #     messages.add_message(request, messages.INFO, 'Car has been sold')
        # super(CarAdmin, self).save_model(request, obj, form, change)

class GymBookingBlockAdmin(admin.ModelAdmin):
    list_display = ('date', 'all_day', 'time', 'duration', 'block_by' )


class CinemaBookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'flat', 'tenant', 'duration', 'made_by' )


class CinemaBookingBlockAdmin(admin.ModelAdmin):
    list_display = ('date', 'made_by')


admin.site.register(GymBooking, GymBookingAdmin)
admin.site.register(GymBookingBlock, GymBookingBlockAdmin)
admin.site.register(CinemaBooking, CinemaBookingAdmin)
admin.site.register(CinemaBookingBlock, CinemaBookingBlockAdmin)

