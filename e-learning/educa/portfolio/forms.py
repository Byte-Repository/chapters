from django import forms
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'content_type', 'content', 'link']
    
    def clean_content(self):
        content_type = self.cleaned_data.get('content_type')
        content = self.cleaned_data.get('content')
        
        if content_type == 'image' and not content.name.endswith('.png'):
            raise forms.ValidationError("Image must be a PNG file.")
        elif content_type == 'video' and not content.name.endswith('.mp4'):
            raise forms.ValidationError("Video must be an MP4 file.")
        elif content_type == 'file' and not content.name.endswith('.pdf'):
            raise forms.ValidationError("File must be a PDF.")
        
        return content
