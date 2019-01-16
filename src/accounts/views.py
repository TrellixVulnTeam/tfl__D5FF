from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            form_error = False

            context['form'] = LoginForm()

            return redirect("/")
        else:
            print("Error")

    return render(request, 'accounts/login.html', context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()

    return render(request, "accounts/register.html", context)
