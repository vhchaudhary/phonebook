from django.db import models
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel


class Contact(TimeStampedModel):
    fname = models.CharField(max_length=30, verbose_name='First Name')
    lname = models.CharField(max_length=30, verbose_name='Sur Name', blank=True, null=True)
    nick_name = models.CharField(max_length=30, verbose_name='Nick Name', null=True, blank=True)
    company_name = models.CharField(max_length=30, null=True, verbose_name='Company', blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    bdate = models.DateField(null=True, verbose_name='Birth Date', blank=True)
    is_favourite = models.BooleanField(default=False, verbose_name='Favourite')

    def __str__(self):
        return self.fname


class ContactNo(TimeStampedModel):
    number = models.CharField(max_length=13)
    number_type = models.CharField(choices=[('mobile', 'Mobile'), ('tel', 'Telephone'), ('fax', 'Fax')],
                                   max_length=6, default='mobile')
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.contact_id.fname + ' - '+ self.number


class Address(TimeStampedModel):
    street = models.TextField(max_length=60)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = CountryField()
    zip = models.CharField(max_length=6)
    type = models.CharField(choices=[('home', 'Home'), ('work', 'Work')], max_length=6)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.type + ' - ' + self.contact_id.fname
