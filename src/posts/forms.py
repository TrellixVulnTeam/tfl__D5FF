from django import forms

from .models import Post
from tfl.forms import MyImagePostWidget


class PostForm(forms.ModelForm):
    image = forms.ImageField(widget=MyImagePostWidget(), label='', required=True)
    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1',
               'id': 'inputDescription',
               'placeholder': 'Description',
               }
    ), label='', required=False)

    class Meta:
        model = Post
        fields = ('image', 'description')

    # def save(self, commit=True):
    #     post = super(PostForm, self).save(commit=False)
    #     print(self.request.user)
    #     # post.user = self.request.user
    #     if commit:
    #         post.save()
    #     return post
