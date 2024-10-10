from django import forms
from .models import Post, Comment, Rating, Image

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

class RecipeForm(forms.ModelForm):
    image = forms.ModelChoiceField(
        queryset=Image.objects.filter(recipe__isnull=True),  # Only show images not yet tied to any recipe
        required=False,
        label="Select an Image"
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'ingredients', 'instructions', 'image']
