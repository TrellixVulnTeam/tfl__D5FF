import datetime

from django import forms
from tempus_dominus.widgets import DateTimePicker

from .models import Cart
from companies.models import Company


class CartForm(forms.ModelForm):
    manifestation = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputManifestation',
               'placeholder': 'Manifestation',
               'name': 'manifestation',
               'onChange': 'cart_field_change(name, value, 0)'
               }
    ), label='')
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputAddress',
               'placeholder': 'Address',
               'name': 'address',
               'onChange': 'cart_field_change(name, value, 0)'
               }
    ), label='')
    beginning = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm',
            'ignoreReadonly': True
        },
        attrs={'class': 'form-control',
               'id': 'inputBiginning',
               'placeholder': 'Beginning Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               'name': 'beginning',
               'readonly': 'readonly',
               'onChange': 'cart_field_change(name, value, 1)'

               }
    ), label='', required=True)
    ending = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm',
            'ignoreReadonly': True
        },
        attrs={'class': 'form-control',
               'id': 'inputEnding',
               'placeholder': 'Ending Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               'name': 'ending',
               'readonly': 'readonly',
               'onChange': 'cart_field_change(name, value, 1)'
               }
    ), label='')
    delivery = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm',
            'ignoreReadonly': True
        },
        attrs={'class': 'form-control',
               'id': 'inputDelivery',
               'placeholder': 'Delivery Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               'name': 'delivery',
               'readonly': 'readonly',
               'onChange': 'cart_field_change(name, value, 1)'
               }
    ), label='')
    pickup = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm',
            'ignoreReadonly': True
        },
        attrs={'class': 'form-control',
               'id': 'inputPickup',
               'placeholder': 'Pickup Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               'name': 'pickup',
               'readonly': 'readonly',
               'onChange': 'cart_field_change(name, value, 1)'
               }
    ), label='')
    personal_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPersonalName',
                                       'placeholder': 'Personal Name',
                                       'name': 'personal_name',
                                       'onChange': 'cart_field_change(name, value, 0)'
                                       }
                                ), label='')
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputEmail',
                                       'placeholder': 'Email',
                                       'name': 'email',
                                       'onChange': 'cart_field_change(name, value, 0)'
                                       }
                                ), label='')

    phone = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPhone',
                                       'placeholder': 'Phone number',
                                       'name': 'phone',
                                       'onChange': 'cart_field_change(name, value, 0)'
                                       }
                                ), label='')

    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label='Company', label='')

    class Meta:
        model = Cart
        fields = ('manifestation',
                  'address',
                  'beginning',
                  'ending',
                  'delivery',
                  'pickup',
                  'personal_name',
                  'email',
                  'phone',
                  'company'
                  )

    def __init__(self, *args, **kwargs):
        cart = kwargs['instance']
        user = cart.user
        if not user.is_admin and not user.is_staff:
            super().__init__(*args, **kwargs)
            self.fields['company'].disabled = True
        else:
            super().__init__(*args, **kwargs)

    def clean_beginning(self):
        beginning = self.cleaned_data.get('beginning')
        date_time_obj = datetime.datetime.strptime(beginning, '%d/%m/%Y %H:%M')

        return date_time_obj

    def clean_ending(self):
        ending = self.cleaned_data.get('ending')
        date_time_obj = datetime.datetime.strptime(ending, '%d/%m/%Y %H:%M')

        return date_time_obj

    def clean_delivery(self):
        delivery = self.cleaned_data.get('delivery')
        date_time_obj = datetime.datetime.strptime(delivery, '%d/%m/%Y %H:%M')

        return date_time_obj

    def clean_pickup(self):
        pickup = self.cleaned_data.get('pickup')
        date_time_obj = datetime.datetime.strptime(pickup, '%d/%m/%Y %H:%M')

        return date_time_obj

    # def save(self, commit=True):
    #     cart = super(CartForm, self).save(commit=False)
    #     if commit:
    #         cart.save()
    #         print('OVO SE POZIVA!!!')
    #     return cart
