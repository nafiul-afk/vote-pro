# FILE: backend/accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Admin Voter Management
    path('admin/voters/', views.admin_voters_list, name='admin_voters_list'),
    path('admin/voters/<int:voter_id>/toggle/', views.toggle_voter_status, name='toggle_voter_status'),
]
