from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Signup, Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('username','email', 'is_active', 'is_admin')
    search_fields = ('email','username')
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
