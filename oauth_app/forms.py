# forms.py
from django import forms
from .models import Wildlife, Post, UploadImage

class WildlifeForm(forms.ModelForm):
    class Meta:
        model = Wildlife
        fields = ['address', 'name', 'image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
from .models import Comment
from django import forms

# from https://djangocentral.com/creating-comments-system-with-django/
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',) #removed email

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']