import datetime

from django import forms
from tempus_dominus.widgets import DateTimePicker

from .models import Cart


class CartForm(forms.ModelForm):
    manifestation = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputManifestation',
               'placeholder': 'Manifestation',
               }
    ), label='')
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputAddress',
               'placeholder': 'Address',
               }
    ), label='')
    beginning = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm:ss'
        },
        attrs={'class': 'form-control',
               'id': 'inputBiginning',
               'placeholder': 'Beginning Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='')
    ending = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm:ss'
        },
        attrs={'class': 'form-control',
               'id': 'inputEnding',
               'placeholder': 'Ending Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='')
    delivery = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm:ss'
        },
        attrs={'class': 'form-control',
               'id': 'inputDelivery',
               'placeholder': 'Delivery Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='')
    pickup = forms.CharField(widget=DateTimePicker(
        options={
            'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
            'useCurrent': False,
            'collapse': False,
            'format': 'DD/MM/YYYY HH:mm:ss'
        },
        attrs={'class': 'form-control',
               'id': 'inputPickup',
               'placeholder': 'Pickup Date',
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
               }
    ), label='')
    personal_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPersonalName',
                                       'placeholder': 'Personal Name',
                                       }
                                ), label='')
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputEmail',
                                       'placeholder': 'Email',
                                       }
                                ), label='')

    phone = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPhone',
                                       'placeholder': 'Phone number',
                                       }
                                ), label='')

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
                  'phone'
                  )

    # def clean_password2(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password and password2 and password2 != password:
    #         raise forms.ValidationError("Password must match!")
    #     return password2

    def save(self, commit=True):
        cart = super(CartForm, self).save(commit=False)
        if commit:
            cart.save()
        return cart
