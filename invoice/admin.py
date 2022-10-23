from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from . models import *


class AccountInline(admin.StackedInline):
    model = Account
    can_delete: False
    verbose_name_plural: 'Account'


class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline,)


admin.site.unregister(User)

admin.site.register(Department)
admin.site.register(Invoice)
admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(PaymentTerm)
admin.site.register(User, CustomizedUserAdmin)
