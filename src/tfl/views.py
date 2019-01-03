from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect

from .forms import LoginForm, RegisterForm

def home_page(request):
    return render(request, 'home_page.html', {})


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     print("User login")
#     print(request.user.is_authenticated)
#     if form.is_valid():
#         print(form.cleaned_data)
#
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#
#         user = authenticate(request, username=username, password=password)
#         print(request.user.is_authenticated)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page.
#             #context['form'] = LoginForm()
#             return redirect("/")
#         else:
#             # Return an 'invalid login' error message.
#             print("Error")
#
#     return render(request, "auth/login.html", context)

def login_page(request):
    # form = LoginForm(request.POST or None)
    # context = {
    #     "form": form
    # }
    # print("User login")
    # print(request.user.is_authenticated)
    # if form.is_valid():
    #     print(form.cleaned_data)

        username = request.POST.get("username")
        password = request.POST.get("password")

        form_error = True

        context = {
            'form_error': form_error
        }

        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            #context['form'] = LoginForm()
            form_error = False

            return redirect("/")
        else:
            # Return an 'invalid login' error message.
            print("Error")
            context['form_error'] = form_error
            return render(request, 'home_page.html', context)


        #return redirect("/")


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "auth/register.html", context)
