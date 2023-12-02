from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    post_content = forms.CharField(label='Tekst Posta:', widget=forms.Textarea())
    image = forms.CharField(label='Zdjęcie', widget=forms.FileInput(attrs={'style':'font-size: 1.55vh'}))
    class Meta:
        model = Post
        fields = ('post_content', 'image')

class CommentModelForm(forms.ModelForm):
    comment_content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Napisz komentarz...'}))
    class Meta:
        model = Comment
        fields = ('comment_content',)