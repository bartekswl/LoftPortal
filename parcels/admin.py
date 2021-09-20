from django.contrib import admin
from .models import Parcel


class ParcelAdmin(admin.ModelAdmin):
    list_display = ('date_arrived', 'flat_number', 'tenant', 'amount_parcels','is_collected', 'parcel_num', 'turnover')

admin.site.register(Parcel, ParcelAdmin)
