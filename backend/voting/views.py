# FILE: backend/voting/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Vote, VoteAuditLog
from elections.models import Election, Candidate
from django.db import transaction

@login_required
def cast_vote(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    election = candidate.election
    voter = getattr(request.user, 'voter_profile', None)

    if not voter:
        messages.error(request, "Voter profile not found.")
        return redirect('accounts:dashboard')

    if voter.is_blocked:
        messages.error(request, "Your account is blocked.")
        return redirect('accounts:dashboard')

    if election.status != 'RUNNING':
        messages.error(request, "This election is not currently running.")
        return redirect('elections:detail', pk=election.id)

    # Atomic transaction to prevent double voting and ensure audit log
    try:
        with transaction.atomic():
            if Vote.objects.filter(voter=voter, election=election).exists():
                messages.error(request, "You have already voted in this election.")
                return redirect('elections:detail', pk=election.id)

            # Create Vote
            Vote.objects.create(voter=voter, election=election, candidate=candidate)
            
            # Create Audit Log
            VoteAuditLog.objects.create(
                voter_username=request.user.username,
                election_title=election.title,
                candidate_name=candidate.name,
                ip_address=get_client_ip(request)
            )

            messages.success(request, f"Successfully voted for {candidate.name}!")
    except Exception as e:
        messages.error(request, "An error occurred while casting your vote.")
        print(f"Vote Error: {e}")

    return redirect('elections:detail', pk=election.id)

@login_required
def election_results(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if election.status != 'FINISHED' and not request.user.is_staff:
        messages.error(request, "Results are only visible after the election ends.")
        return redirect('elections:detail', pk=election.id)

    candidates = election.candidates.all()
    total_votes = election.votes.count()
    
    # Simple winner logic
    winner = None
    if total_votes > 0:
        winner = max(candidates, key=lambda c: c.vote_count)

    return render(request, 'voting/results.html', {
        'election': election,
        'candidates': candidates,
        'total_votes': total_votes,
        'winner': winner
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
