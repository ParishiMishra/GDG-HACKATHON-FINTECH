from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Root URL for the portfolio app
    path('dashboard/', views.dashboard, name='dashboard'),  # Add this line
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('portfolio/add/', views.add_portfolio, name='add_portfolio'),
    path('portfolio/<int:portfolio_id>/add_investment/', views.add_investment, name='add_investment'),
]