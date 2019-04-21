from .utils import generate_menu


def get_menu(request):
    user = request.user
    data = generate_menu(user)

    request.session['companies_menu'] = data['companies_menu']

    return data
