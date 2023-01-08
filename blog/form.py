from django import forms
from .models import Blog, Comment, Like


# ブログフォーム
class BlogForm(forms.ModelForm):
    class Meta():
        model = Blog
        fields = ('title', 'feeling', 'memory_image')

    feeling = forms.CharField(
        required=False,
        max_length=1200,
        label='感想',
        widget=forms.Textarea(
            attrs={
                'placeholder': '感想を記述してください',
            }
        )
    )


# コメントフォーム
class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('comment',)
    comment = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'rows': 5,
            }
        )
    )
