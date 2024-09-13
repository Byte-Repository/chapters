from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()

class RatingForm(forms.Form):
    score = forms.IntegerField(
        min_value=1, 
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Rate this recipe from 1 to 5"
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        help_text="Optional: Leave a comment with your rating"
    )