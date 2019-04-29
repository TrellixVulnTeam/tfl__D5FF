from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.http import JsonResponse

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'


class ChartDataView(LoginRequiredMixin, APIView):

    def get(self, request, format=None):

        users_number = User.objects.all().count()

        data = {
            "users": users_number
        }
        return Response(data)

