from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse

from .signals import user_logged_in
from .models import UsernameActivation
from companies.models import Company

User = get_user_model()


class ReactivateUsernameForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputUsername',
               'placeholder': 'Username',
               }
    ), label='')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = UsernameActivation.objects.username_exists(username)
        if not qs.exists():
            register_link = reverse('register')
            msg = ''''This username does not exist would you like to <a href='{link}'>register</a>?
            '''.format(link=register_link)
            return forms.ValidationError(mark_safe(msg))
        return username


class UserDetailChangeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputEmail',
                                       'placeholder': 'Email',
                                       }
                                ), label='', disabled=True)
    username = forms.CharField(widget=forms.TextInput(
                                    attrs={'class': 'form-control mb-1',
                                           'id': 'inputUsername',
                                           'placeholder': 'Username',
                                           }
                                    ), label='', disabled=True)
    # company = forms.CharField(widget=forms.TextInput(
    #                                 attrs={'class': 'form-control mb-1',
    #                                        'id': 'inputCompany',
    #                                        'placeholder': 'Company',
    #                                        }
    #                             ), label='', disabled=True)
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label='Company', label='', disabled=False)
    personal_name = forms.CharField(widget=forms.TextInput(
                                        attrs={'class': 'form-control mb-1',
                                               'id': 'inputPersonalName',
                                               'placeholder': 'Personal Name',
                                               }
                                        ), label='')
    address = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputAddress',
                                       'placeholder': 'Address',
                                       }
                                ), label='')
    phone = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPhone',
                                       'placeholder': 'Phone number',
                                       }
                                ), label='')

    class Meta:
        model = User
        fields = ('email', 'username', 'company', 'personal_name', 'address', 'phone',)

    # def __init__(self, *args, **kwargs):
    #     user = kwargs['instance']
    #     print(user.company)
    #     if user.company is not None:
    #         company_name = user.company.name
    #         kwargs.update(initial={
    #             'company': company_name
    #         })
    #         super().__init__(*args, **kwargs)
    #     else:
    #         super().__init__(*args, **kwargs)
    #         # self.fields['company'].disabled = False
    #         # self.fields['company']
    def __init__(self, *args, **kwargs):
        user = kwargs['instance']
        super().__init__(*args, **kwargs)
        if user.company is not None:
            self.fields['company'].disabled = True


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputUsername',
                                       'placeholder': 'Username',
                                       }
                                ), label='')
    password = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class': 'form-control mb-5',
                                       'id': 'inputPassword',
                                       'placeholder': 'Password',
                                       }
                                ), label='')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    # @property
    def clean(self):
        request = self.request
        # data = self.cleaned_data
        # username = data.get('username')
        # password = data.get('password')
        #
        # cleaned_data = super().clean()
        # cc_myself = cleaned_data.get("cc_myself")
        # subject = cleaned_data.get("subject")

        data = super().clean()
        username = data.get('username', None)
        password = data.get('password', None)

        qs = User.objects.filter(username=username)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse('account:resend_activation')
                reconfirm_msg = '''Please <a href='{resend_link}'>
                go here to resend activation!</a>.
                '''.format(resend_link=link)
                confirm_username = UsernameActivation.objects.filter(username=username)
                is_confirmable = confirm_username.confirmable().exists()
                if is_confirmable:
                    raise forms.ValidationError('Your account is not activated yet!')
                username_confirm_exists = UsernameActivation.objects.username_exists(username).exists()
                if username_confirm_exists:
                    raise forms.ValidationError(mark_safe(reconfirm_msg))
                if not is_confirmable and not username_confirm_exists:
                    raise forms.ValidationError('This user not registered.')

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid credentials. Wrong username and/or password!', code='invalid')

        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=request)
        return data


class RegisterForm(forms.ModelForm):
    personal_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPersonalName',
                                       'placeholder': 'Personal Name',
                                       }
                                ), label='')
    username = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputUsername',
                                       'placeholder': 'Username',
                                       }
                                ), label='')
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputEmail',
                                       'placeholder': 'Email',
                                       }
                                ), label='')
    address = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputAddress',
                                       'placeholder': 'Address',
                                       }
                                ), label='')
    phone = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPhone',
                                       'placeholder': 'Phone number',
                                       }
                                ), label='')
    password = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class': 'form-control mb-1',
                                       'id': 'inputPassword',
                                       'placeholder': 'Password',
                                       }
                                ), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class': 'form-control mb-5',
                                       'id': 'inputPassword',
                                       'placeholder': 'Confirm password',
                                       }
                                ), label='')

    class Meta:
        model = User
        fields = ('personal_name', 'username', 'email', 'address', 'phone',)

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password2 != password:
            raise forms.ValidationError("Password must match!")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # send confirmation email via signals
        if commit:
            user.save()
        return user
