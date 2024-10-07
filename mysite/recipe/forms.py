from django import forms
from .models import Comment
from .models import Rating

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']