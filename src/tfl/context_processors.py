from .utils import generate_menu


def get_menu(request):
    user = request.user
    data = generate_menu(user)

    return data
