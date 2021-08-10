from django.contrib import admin
from .models import Parcel


class ParcelAdmin(admin.ModelAdmin):
    list_display = ('date_arrived', 'flat_number', 'tenant', 'tenant', 'is_collected', 'parcel_num')

admin.site.register(Parcel, ParcelAdmin)
