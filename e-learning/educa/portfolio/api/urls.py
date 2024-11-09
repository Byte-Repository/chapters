from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # List and Create Portfolio Entries (Authenticated Users)
    path('portfolio_entries/', views.PortfolioListCreateView.as_view(), name='portfolio_list_create'),
    
    # Retrieve a Specific Portfolio Entry (Authenticated Users)
    path('portfolio_entries/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
]
