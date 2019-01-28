from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin
from .forms import LoginForm, RegisterForm, ReactivateUsernameForm
from .models import UsernameActivation
from tfl.mixins import NextUrlMixin, RequestFormAttachMixin

class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUsernameActivateView(FormMixin, View):
    success_url = '/login'
    form_class = ReactivateUsernameForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = UsernameActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = qs.first()
                obj.activate()
                messages.success(request, 'Username has been confirmed!')
                return redirect('login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    msg = 'This username has alredy been confirmed'
                    messages.success(request, mark_safe(msg))
                    return redirect('login')
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation_error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = 'Username has been confirmed!'
        request = self.request
        messages.success(request, msg)
        username = form.cleaned_data.get('username')
        obj = UsernameActivation.objects.username_exists(username).first()
        user = obj.user
        new_activation = UsernameActivation.objects.create(user=user, username=username)
        new_activation.send_activation()
        return super(AccountUsernameActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, 'key': self.key}
        return render(self.request, 'registration/activation_error.html', context)


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = '/login/'

