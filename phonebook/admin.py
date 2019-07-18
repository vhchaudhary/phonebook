from django.contrib import admin
from .models import *


class ContactNoInline(admin.TabularInline):
    model = ContactNo


class AddressInline(admin.TabularInline):
    model = Address


class ContactAdmin(admin.ModelAdmin):

    list_display = ['fname', 'lname', 'bdate', 'is_favourite']
    inlines = [ContactNoInline, AddressInline]


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactNo)
admin.site.register(Address)