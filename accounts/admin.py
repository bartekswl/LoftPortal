from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PortalUser



class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'flat', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )





    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)

admin.site.register(PortalUser, AccountAdmin)


