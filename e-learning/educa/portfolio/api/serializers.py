from rest_framework import serializers
from portfolio.models import Portfolio  # Correct import

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'date', 'content_type', 'content', 'link', 'course', 'student']
        read_only_fields = ['student']  # Ensure that 'student' is read-only
