from django import forms
from .models import Profile
from posts.models import Comment


class ProfileModelForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')


class CommentModelForm(forms.ModelForm):
    comment_content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Napisz komentarz...'}))
    class Meta:
        model = Comment
        fields = ('comment_content',)