from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputName',
               'placeholder': 'Company Name',
               }
    ), label='', required=True)

    class Meta:
        model = Company
        fields = ('name', )
