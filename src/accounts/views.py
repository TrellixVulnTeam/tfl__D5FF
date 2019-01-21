from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .forms import LoginForm, RegisterForm
from .models import UsernameActivation


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUsernameActivateView(View):
    def get(self, request, key, *args, **kwargs):
        qs = UsernameActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj = qs.first()
            obj.activate()
            messages.success(request, 'Username has been confirmed')
            return redirect('login')
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                msg = 'This username has alredy been confirmed'
                messages.success(request, mark_safe(msg))
                return redirect('login')
        return render(request, 'registration/activation_error.html')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, 'This user is inactive')
                return super(LoginView, self).form_invalid(form)
            login(request, user)
            return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = '/login/'

