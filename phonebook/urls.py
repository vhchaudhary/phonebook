
from django.urls import path
from .views import *

app_name = 'phone_book'

urlpatterns = [
    path('logins/', logins, name='login'),
    path('log_out/', log_out, name='logout'),
    path('tog_fav/<int:id>', toggle_favourite, name='tog_fav'),
    path('del_contact/<int:id>', delete_contact, name='del_contact'),
    path('update_cn_md/<int:id>', update_contact_modal, name='update_cn_md'),
    path('update_contact', update_contact, name='update_contact'),
    path('all/', ContactDetails.as_view(), name='contact_details'),
    path('update/<int:pk>', ContactUpdate.as_view(), name='contact_update'),
]
