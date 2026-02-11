# FILE: backend/voting/urls.py

from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('cast/<int:candidate_id>/', views.cast_vote, name='cast_vote'),
    path('results/<int:election_id>/', views.election_results, name='results'),
]
