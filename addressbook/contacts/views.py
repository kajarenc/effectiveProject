from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.core.urlresolvers import reverse

from contacts.models import Contact
import forms


class ListContactView(ListView):
    model = Contact
    template_name = 'contact_list.html'


class CreateContactView(CreateView):
    model = Contact
    template_name = 'edit_contact.html'
 #   form_class = forms.ContactForm
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')
        return context


class UpdateContactView(UpdateView):
    model = Contact
    template_name = 'edit_contact.html'
  #  form_class = forms.ContactForm
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit', kwargs={'pk': self.get_object().id})
        return context


class ContactView(DetailView):
    model = Contact
    template_name = 'contact.html'


class DeleteContactView(DeleteView):
    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')