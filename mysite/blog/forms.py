from django import forms
from .models import Comment

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

# class RecipeCommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['name', 'email', 'body']
#         widgets = {
#             'body': forms.Textarea(attrs={'rows': 3}),
#         }

class SearchForm(forms.Form):
    query = forms.CharField()

# class RatingForm(forms.Form):
#     score = forms.ChoiceField(
#         choices=[(i, i) for i in range(1, 6)],
#         widget=forms.RadioSelect(attrs={'class': 'rating'}),
#         help_text="Rate this recipe from 1 to 5"
#     )
#     comment = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         help_text="Optional: Leave a comment with your rating"
#     )
