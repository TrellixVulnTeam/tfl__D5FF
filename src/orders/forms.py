import datetime

from django import forms
from tempus_dominus.widgets import DateTimePicker

from companies.models import Company


class OrderForm(forms.Form):
    manifestation = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputManifestation',
               'placeholder': 'Manifestation',
               }
    ), label='', disabled=True)
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputAddress',
               'placeholder': 'Address',
               }
    ), label='', disabled=True)
    beginning = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm'
        },
        attrs={'class': 'form-control',
               'id': 'inputBiginning',
               'placeholder': 'Beginning Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='', disabled=True)
    ending = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm'
        },
        attrs={'class': 'form-control',
               'id': 'inputEnding',
               'placeholder': 'Ending Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='', disabled=True)
    delivery = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm'
        },
        attrs={'class': 'form-control',
               'id': 'inputDelivery',
               'placeholder': 'Delivery Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='', disabled=True)
    pickup = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm'
        },
        attrs={'class': 'form-control',
               'id': 'inputPickup',
               'placeholder': 'Pickup Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='', disabled=True)
    personal_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPersonalName',
                                       'placeholder': 'Personal Name',
                                       }
                                ), label='', disabled=True)
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputEmail',
                                       'placeholder': 'Email',
                                       }
                                ), label='', disabled=True)

    phone = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPhone',
                                       'placeholder': 'Phone number',
                                       }
                                ), label='', disabled=True)

    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label='Company', label='', disabled=True)

    # class Meta:
    #     model = Cart
    #     fields = ('manifestation',
    #               'address',
    #               'beginning',
    #               'ending',
    #               'delivery',
    #               'pickup',
    #               'personal_name',
    #               'email',
    #               'phone'
    #               )
    #
    # def clean_beginning(self):
    #     beginning = self.cleaned_data.get('beginning')
    #     date_time_obj = datetime.datetime.strptime(beginning, '%d/%m/%Y %H:%M')
    #
    #     return date_time_obj
    #
    # def clean_ending(self):
    #     ending = self.cleaned_data.get('ending')
    #     date_time_obj = datetime.datetime.strptime(ending, '%d/%m/%Y %H:%M')
    #
    #     return date_time_obj
    #
    # def clean_delivery(self):
    #     delivery = self.cleaned_data.get('delivery')
    #     date_time_obj = datetime.datetime.strptime(delivery, '%d/%m/%Y %H:%M')
    #
    #     return date_time_obj
    #
    # def clean_pickup(self):
    #     pickup = self.cleaned_data.get('pickup')
    #     date_time_obj = datetime.datetime.strptime(pickup, '%d/%m/%Y %H:%M')
    #
    #     return date_time_obj

    # def save(self, commit=True):
    #     cart = super(CartForm, self).save(commit=False)
    #     if commit:
    #         cart.save()
    #         print('OVO SE POZIVA!!!')
    #     return cart
