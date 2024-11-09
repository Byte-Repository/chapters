from rest_framework import generics, permissions
from portfolio.models import Portfolio
from portfolio.api.serializers import PortfolioSerializer
from portfolio.api.permissions import IsInstructorOrAdmin, IsStudent

# View to list and create portfolio entries
class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer  # Make sure this matches the imported serializer name
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access this view

    def get_queryset(self):
        # If the user is staff (instructor/admin), return all portfolio entries
        if self.request.user.is_staff:
            return Portfolio.objects.all()
        # If the user is a student, return only their entries
        return Portfolio.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        # Set the student as the current user when creating a portfolio entry
        serializer.save(student=self.request.user)

# View to retrieve individual portfolio entries
class PortfolioDetailView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer  # Use the correct serializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]  # Only the student can view their portfolio
