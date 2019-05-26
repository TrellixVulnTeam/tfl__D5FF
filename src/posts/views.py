from django.views.generic import ListView, FormView, CreateView, DeleteView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse

from tfl.mixins import NextUrlMixin

from .models import Post
from .forms import PostForm


class PostView(ListView, FormView):
    form_class = PostForm
    template_name = "posts/home.html"
    #success_url = '/cart/'

    def get_queryset(self):
        return Post.objects.all()

    # def form_valid(self, form):
    #     form.save()
    #     return redirect(self.success_url)


# class PostAddView(CreateView):
#     form_class = PostForm
#     template_name = "posts/home.html"
#     success_url = '/cart/'
#
#
#     def get_queryset(self):
#         return Post.objects.all()

def post_add(request):
    if request.method == 'POST':
        success_url = '/'
        form = PostForm(request.POST or None, request.FILES or None)
        # print(form.is_valid())
        if form.is_valid():
            Post.objects.new(user=request.user, form=form)
            return redirect(success_url)
    return HttpResponseServerError('GRESKAAAAA')


def post_remove(request):
    user = request.user
    if request.method == 'POST' and (user.is_staff or user.is_admin):
        post_id = request.POST.get('post_id')
        if post_id is not None:
            Post.objects.remove(post_id)
    return redirect('/')


# class CartRemoveView(NextUrlMixin, DeleteView):
#     form_class = PostForm
#     template_name = 'posts/home.html'
#     success_url = '/'
#
#     def get_object(self, queryset=None):
#         request = self.request
#         post_id = request.POST.get('post_id')
#         if post_id is not None:
#             try:
#                 post_obj = Post.objects.get(id=post_id)
#                 post_obj.active = False
#                 post_obj.save()
#             except Post.DoesNotExist:
#                 return redirect('/')
#         return None
#
#     def get_success_url(self):
#         return reverse('/')
