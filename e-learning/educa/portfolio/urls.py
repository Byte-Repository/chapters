from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/upload/', views.portfolio_upload, name='portfolio_upload'),
    path('course/<int:course_id>/portfolios/', views.portfolio_list, name='portfolio_list'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
]
