from django.contrib import admin
from .models import *


# override admin.Tablularline for diplay multiple numbers, you can also use StackedInline
class ContactNoInline(admin.TabularInline):
    model = ContactNo


# ModelAdmin provide basic customization to admin like searching, listing, filtering etc...
class ContactAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'bdate', 'is_favourite']
    inlines = [ContactNoInline]


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactNo)
admin.site.register(Address)