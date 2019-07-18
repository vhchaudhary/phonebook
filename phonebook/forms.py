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
    bdate = forms.DateField(label='Birth Date', required=False, widget=forms.TextInput(attrs={
        'type': 'date',
    }))

    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = True
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3 create-label'
        # self.helper.field_class = 'col-md-8'
        # self.helper.layout = Layout(
        #     Div(
        #         Field('fname'),
        #         Field('lname'),
        #         Field('email'),),
        #     Div(
        #         Field('bdate'),
        #         Field('company_name'),
        #         Field('website'),
        #         Fieldset('Add Contacts',
        #                  Formset('contacts')),
        #         HTML("<br>"),
        #         ButtonHolder(Submit('submit', 'save')),
        #     )
        # )

        self.helper.layout = Layout(
            Row(
                Column('fname', css_class='form-group col-md-6 mb-0'),
                Column('lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('bdate', css_class='form-group col-md-6 mb-0'),
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('website', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Fieldset('Add Contact Numbers', Formset('contacts')),
            Submit('submit', 'Save')
        )


class ContactNoForm(forms.ModelForm):
    class Meta:
        model = ContactNo
        exclude = ()


ContactNoFormSet = inlineformset_factory(
    Contact, ContactNo, form=ContactNoForm,
    fields=['number', 'number_type'], extra=1, can_delete=True
)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['contact_id']

