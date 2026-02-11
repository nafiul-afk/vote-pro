# FILE: backend/accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import VoterRegistrationForm
from .models import Voter
from elections.models import Election

def home(request):
    return render(request, 'public/home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('accounts:login')
    else:
        form = VoterRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    voter = getattr(request.user, 'voter_profile', None)
    if not voter and not request.user.is_staff:
        # If no profile exists for some reason, create one or handle
        messages.error(request, "Voter profile not found.")
        return redirect('accounts:home')
    
    if voter and voter.is_blocked:
        messages.error(request, "Your account has been blocked. Please contact admin.")
        logout(request)
        return redirect('accounts:login')

    upcoming_elections = Election.objects.filter(status='UPCOMING')[:5]
    running_elections = Election.objects.filter(status='RUNNING')
    
    context = {
        'upcoming': upcoming_elections,
        'running': running_elections,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

# Admin Voter Management
@user_passes_test(lambda u: u.is_staff)
def admin_voters_list(request):
    voters = Voter.objects.all().select_related('user')
    return render(request, 'accounts/admin_voters.html', {'voters': voters})

@user_passes_test(lambda u: u.is_staff)
def toggle_voter_status(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)
    voter.status = 'BLOCKED' if voter.status == 'ACTIVE' else 'ACTIVE'
    voter.save()
    messages.success(request, f"Status for {voter.user.username} updated to {voter.status}.")
    return redirect('accounts:admin_voters_list')
