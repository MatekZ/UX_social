from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_content', 'image')

class CommentModelForm(forms.ModelForm):
    comment_content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Napisz komentarz...'}))
    class Meta:
        model = Comment
        fields = ('comment_content',)