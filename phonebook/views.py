
import vobject
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView
from .forms import *
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .document import *


class ContactDetails(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'phonebook/contact_data.html'
    form_class = ContactForm
    success_url = None
    login_url = '/logins/'

    def get_context_data(self, **kwargs):
        contacts = ContactDocument.search(index='contacts').scan()
        contact_data = [
            {
                'id': c.id,
                'name': c.fname + ' ' + (c.lname if c.lname else ''),
                'email': c.email if c.email else '-',
                'is_favourite': c.is_favourite,
                'ph_numbers': [cn.number for cn in ContactNo.objects.filter(contact_id=c.id)]
            }
            for c in contacts
        ]
        kwargs.update({'data': contact_data})
        data = super(ContactDetails, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contacts'] = ContactNoFormSet(self.request.POST)
        else:
            data['contacts'] = ContactNoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        numbers = context['contacts']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if numbers.is_valid():
                numbers.instance = self.object
                numbers.save()
        return super(ContactDetails, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('phone_book:contact_details')


class ContactUpdate(UpdateView):
    model = Contact
    template_name = 'phonebook/contact_data.html'
    form_class = ContactForm
    success_url = None

    def get_context_data(self, **kwargs):
        contacts = ContactDocument.search(index='contacts').scan()
        contact_data = [
            {
                'id': c.id,
                'name': c.fname + ' ' + (c.lname if c.lname else ''),
                'email': c.email if c.email else '-',
                'is_favourite': c.is_favourite,
                'ph_numbers': [cn.number for cn in ContactNo.objects.filter(contact_id=c.id)]
            }
            for c in contacts
        ]
        kwargs.update({'data': contact_data})
        data = super(ContactUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contacts'] = ContactNoFormSet(self.request.POST, instance=self.object)
        else:
            data['contacts'] = ContactNoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        numbers = context['contacts']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if numbers.is_valid():
                numbers.instance = self.object
                numbers.save()
        return super(ContactUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('phone_book:contact_details', kwargs={'pk': self.object.pk})


def logins(request):
    if request.user.id and request.user.is_authenticated:
        return redirect('phone_book:contact_details')
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('phone_book:contact_details')
            else:
                return redirect('phone_book:login')
    else:
        login_form = LoginForm()
        return render(request, 'phonebook/login.html', {'form': login_form})


def log_out(request):
    logout(request)  # It will logout user and clear current login sessions
    return redirect('phone_book:login')


@login_required
def delete_contact(request, id):
    """ This method use for delete contact to favourite and its request type is AJAX """
    contact = Contact.objects.get(pk=id)
    contact.delete()
    return JsonResponse({'success': True})


@login_required
def toggle_favourite(request, id):
    """ This method use for add contact to favourite and its request type is AJAX """
    contact = Contact.objects.get(pk=id)
    contact.is_favourite = not contact.is_favourite
    contact.save()
    return JsonResponse({'success': True, 'fav_value': contact.is_favourite})


def delete_multi(request):
    if request.POST and request.is_ajax:
        contact_ids = dict(request.POST).get("ids[]")
        contacts = Contact.objects.filter(pk__in=contact_ids)
        print("Contacts", [c.fname for c in contacts])
        # contacts.delete()
        return JsonResponse({"success": True, "contacts": contact_ids})


@login_required
def import_vcf(request):
    if request.is_ajax() and request.method == "POST" and request.FILES:
        file = request.FILES.get('vcf_file')
        if file and file.name[-4:] in ['.vcf', '.csv']:
            with file as f:
                # import pdb
                # pdb.set_trace()
                vc = vobject.readComponents(f.read().decode("utf-8"))
                vo = next(vc, None)
                while vo is not None:
                    # vo.prettyPrint()
                    fname = vo.contents.get('fn')[0].value
                    email = vo.contents.get('email')[0].value if vo.contents.get('email') else ''
                    numbers = []
                    if vo.contents.get('tel'):
                        for v in vo.contents['tel']:
                            no = v.value.replace("-", "")
                            if no not in numbers and no[-10:] not in numbers[-10:]:
                                numbers.append(no)
                    print(fname, ', ', numbers, ', ', email)
                    vo = next(vc, None)
                    # TODO: Bulk creation and code optimization
                    contact = Contact.objects.create(fname=fname, email=email)
                    if numbers:
                        for number in numbers:
                            ContactNo.objects.create(number=number, number_type='mobile', contact_id=contact)

            return redirect("phone_book:contact_details")

        else:
            return JsonResponse({'success': False, 'message': 'Only vcf or csv files are allowed'})
    else:
        return JsonResponse({'success': False})


def contact_data(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        contact_no_form = ContactNoForm(request.POST)
        if contact_form.is_valid() and contact_no_form.is_valid():
            fname = contact_form.cleaned_data.get('fname')
            lname = contact_form.cleaned_data.get('lname')
            nick_name = contact_form.cleaned_data.get('nick_name')
            email = contact_form.cleaned_data.get('email')
            website = contact_form.cleaned_data.get('website')
            company_name = contact_form.cleaned_data.get('company_name')
            bdate = contact_form.cleaned_data.get('bdate')

            number = contact_no_form.cleaned_data.get('number')
            number_type = contact_no_form.cleaned_data.get('number_type')

            contact = Contact.objects.create(fname=fname, lname=lname, nick_name=nick_name, email=email,
                                             website=website, company_name=company_name, bdate=bdate)

            ContactNo.objects.create(number=number, number_type=number_type, contact_id=contact)

    contact_form = ContactForm()
    contact_no_form = ContactNoForm()

    contacts = Contact.objects.all()
    contact_data = [
        {
            'id': c.id,
            'name': c.fname + ' ' + (c.lname if c.lname else ''),
            'email': c.email,
            'is_favourite': c.is_favourite,
            'ph_numbers': [cn.number for cn in ContactNo.objects.filter(contact_id=c.id)]
        }
        for c in contacts
    ]

    return render(request, 'phonebook/contact_data.html', {'contacts': contact_data, 'contact_form': contact_form,
                                                           'contact_no_form': contact_no_form})
