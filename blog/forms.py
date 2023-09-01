from django import forms
from .models import PostComment, NewsComment

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('body', 'owner')

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ('body', 'owner')