from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


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
        user.active = False

        if commit:
            user.save()
        return user



    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     qs = User.objects.filter(username=username)
    #     if qs.exists():
    #         raise forms.ValidationError("Username is taken")
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     qs = User.objects.filter(email=email)
    #     if qs.exists():
    #         raise forms.ValidationError("Email is taken")
    #     return email
    #
    # def clean(self):
    #     data = self.cleaned_data
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password2 != password:
    #         raise forms.ValidationError("Password must match!")
    #     return data
