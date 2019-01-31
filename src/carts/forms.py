from django import forms

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
    beginning = forms.CharField(widget=forms.DateTimeInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputBiginning',
               'placeholder': 'Beginning Date',
               }
    ), label='')
    ending = forms.CharField(widget=forms.DateTimeInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputEnding',
               'placeholder': 'Ending Date',
               }
    ), label='')
    delivery = forms.CharField(widget=forms.DateTimeInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputDelivery',
               'placeholder': 'Delivery Date',
               }
    ), label='')
    pickup = forms.CharField(widget=forms.DateTimeInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputPickup',
               'placeholder': 'Pickup Date',
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
