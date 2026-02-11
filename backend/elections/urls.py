# FILE: backend/elections/urls.py

from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    path('', views.election_list, name='list'),
    path('<int:pk>/', views.election_detail, name='detail'),
    
    # Admin
    path('admin/', views.admin_election_dashboard, name='admin_dashboard'),
    path('admin/create/', views.create_election, name='create'),
    path('admin/<int:pk>/edit/', views.edit_election, name='edit'),
    path('admin/<int:election_id>/add-candidate/', views.add_candidate, name='add_candidate'),
]
