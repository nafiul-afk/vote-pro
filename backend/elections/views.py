# FILE: backend/elections/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Election, Candidate
from .forms import ElectionForm, CandidateForm
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def election_list(request):
    query = request.GET.get('q', '')
    elections_list = Election.objects.all()
    if query:
        elections_list = elections_list.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    paginator = Paginator(elections_list, 10) # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'elections/list.html', {'page_obj': page_obj, 'query': query})

@login_required
def election_detail(request, pk):
    election = get_object_or_404(Election, pk=pk)
    candidates = election.candidates.all()
    
    # Check if voter already voted in this election
    user_voted = False
    if hasattr(request.user, 'voter_profile'):
        from voting.models import Vote
        user_voted = Vote.objects.filter(voter=request.user.voter_profile, election=election).exists()
    
    context = {
        'election': election,
        'candidates': candidates,
        'user_voted': user_voted,
    }
    return render(request, 'elections/detail.html', context)

# Admin Election Management
@user_passes_test(lambda u: u.is_staff)
def admin_election_dashboard(request):
    elections = Election.objects.all()
    return render(request, 'elections/admin_dashboard.html', {'elections': elections})

@user_passes_test(lambda u: u.is_staff)
def create_election(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election created successfully.')
            return redirect('elections:admin_dashboard')
    else:
        form = ElectionForm()
    return render(request, 'elections/election_form.html', {'form': form, 'title': 'Create Election'})

@user_passes_test(lambda u: u.is_staff)
def edit_election(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election updated successfully.')
            return redirect('elections:admin_dashboard')
    else:
        form = ElectionForm(instance=election)
    return render(request, 'elections/election_form.html', {'form': form, 'title': 'Edit Election'})

@user_passes_test(lambda u: u.is_staff)
def add_candidate(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()
            messages.success(request, f'Candidate {candidate.name} added to {election.title}.')
            return redirect('elections:admin_dashboard')
    else:
        form = CandidateForm()
    return render(request, 'elections/candidate_form.html', {'form': form, 'election': election})
