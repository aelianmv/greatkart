from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from . models import Account

class AccountAdmin(UserAdmin):
    list_display = ('first_name','email','username','last_name','is_active','last_login','date_joined')
    filter_horizontal=()
    list_filter=()
    fieldsets =()
    list_display_links=('email','first_name')
    readonly_fields=('date_joined','last_login')
    ordering=('-date_joined',)
    

admin.site.register(Account,AccountAdmin)
