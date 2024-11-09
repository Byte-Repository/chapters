# portfolio/admin.py

from django.contrib import admin
from .models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'content_type', 'course', 'student')  # Columns to display
    list_filter = ('content_type', 'course')  # Filter options for the admin
    search_fields = ('title', 'course__name', 'student__username')  # Searchable fields

admin.site.register(Portfolio, PortfolioAdmin)
