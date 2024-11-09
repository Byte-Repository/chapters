# portfolio/models.py

from django.db import models
from django.conf import settings
from courses.models import Course  # Import the Course model correctly

class Portfolio(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image (PNG)'),
        ('video', 'Video (MP4)'),
        ('file', 'File (PDF)'),
    ]
    
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    content = models.FileField(upload_to='portfolio/')
    # link = models.URLField(blank=True, null=True)
    
    # Relationships
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Fixed the reference here
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
