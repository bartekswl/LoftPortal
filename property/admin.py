from django.contrib import admin
from .models import Flat, Tenant, CommercialUnit, Concierge



class FlatAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superadmin:
                return True
            else:
                return False

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superadmin:
                return True
            else:
                return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_superadmin:
            return True
        else:
            return False

    list_display = ('flat_number', 'building', 'core', 'floor', 'flat_type', 'agency')
    list_display_links = ('flat_number', 'building', 'core')
    
    ordering = ('flat_number',)

    filter_horizontal = ()
    list_filter = ('building','core', 'floor', 'flat_type')
    fieldsets = ()


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'flat', 'status', 'date_added','date_moved_in','moved_out', 'pin_code')



class ConciergeAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superadmin:
                return True
            else:
                return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_superadmin:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superadmin:
                return True
            else:
                return False

    #list_display = ('name', 'surname', 'work_pattern', 'phone_number')




admin.site.register(Flat, FlatAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(CommercialUnit)
admin.site.register(Concierge, ConciergeAdmin)