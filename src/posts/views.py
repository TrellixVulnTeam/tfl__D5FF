from django.views.generic import ListView, FormView, CreateView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseServerError

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
        if form.is_valid():
            Post.objects.new(user=request.user, form=form)
            return redirect(success_url)
    return HttpResponseServerError('GRESKAAAAA')
