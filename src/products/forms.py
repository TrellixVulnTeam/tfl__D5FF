from django import forms

from .models import Product, ProductCategory
from companies.models import Company


class ProductForm(forms.ModelForm):
    image = forms.ImageField()
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputTitle',
               'placeholder': 'Title',
               }
    ), label='', required=True)
    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputDescription',
               'placeholder': 'Description',
               }
    ), label='', required=False)
    # company = forms.ChoiceField()
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label='Company', label='')
    price = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputPrice',
               'placeholder': 'Price',
               }
    ), label='')
    weight = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputWeight',
               'placeholder': 'Weight',
               }
    ), label='')
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), empty_label='Category', label='')
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputLocation',
               'placeholder': 'Location',
               }
    ), label='', required=False)
    quantity = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputQuantity',
               'placeholder': 'Quantity',
               }
    ), label='')

    class Meta:
        model = Product
        fields = (
            'image',
            'title',
            'description',
            'company',
            'price',
            'weight',
            'category',
            'location',
            'quantity'
        )

    # def __init__(self, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #
    #     choices_category = [(category, category.name)
    #                         for category in ProductCategory.objects.all()]
    #     choices_company = [(company, company.name)
    #                        for company in Company.objects.all()]
    #
    #     self.fields['category'] = forms.ChoiceField(widget=forms.Select(
    #         attrs={'class': 'form-control mb-1',
    #                'id': 'inputCategory',
    #                'placeholder': 'Category',
    #               }), choices=choices_category, label='', required=True)
    #     self.fields['company'] = forms.ChoiceField(widget=forms.Select(
    #         attrs={'class': 'form-control mb-1',
    #                'id': 'inputCompany',
    #                'placeholder': 'Company',
    #                }), choices=choices_company, label='', required=True)

    # def save(self, commit=True):
    #     product = super(ProductForm, self).save(commit=False)
    #     category_id = self.cleaned_data['category']
    #     company_id = self.cleaned_data['company']
    #     category_obj = ProductCategory.objects.get_by_id(category_id)
    #     company_obj = Company.objects.get_by_id(company_id)
    #     product.category = category_obj
    #     product.company = company_obj
    #     if commit:
    #         product.save()
    #     return product
