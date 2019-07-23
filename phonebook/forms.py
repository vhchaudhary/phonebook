from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from .custom_layout_object import *
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit, Row, Column


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={
        'type': 'password'
    }))

    class Meta:
        model = User
        fields = ['email', 'password']


class ContactForm(forms.ModelForm):
    bdate = forms.DateField(label='Birth Date', required=False, widget=forms.TextInput(
        attrs={
            'type': 'date',
        })) # Require to show date widget in form

    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # form helper use for custom designing and add bootstrap classes dynamiccaly into forms after render into html
        self.helper.layout = Layout(
            Row(
                Column('fname', css_class='form-group col-md-6 mb-0'),
                Column('lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('bdate', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                Column('website', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Fieldset('Add Contact Numbers', Formset('contacts')),
            Submit('submit', 'Save')
        )


class ContactNoForm(forms.ModelForm):
    class Meta:
        model = ContactNo
        exclude = () # we can also use fields = '__all__'


ContactNoFormSet = inlineformset_factory(
    Contact, ContactNo, form=ContactNoForm,
    fields=['number', 'number_type'], extra=1, can_delete=True
)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['contact_id']
