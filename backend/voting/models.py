# FILE: backend/voting/models.py

from django.db import models
from accounts.models import Voter
from elections.models import Election, Candidate

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='votes_cast')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Enforce that a voter can only vote once per election
        unique_together = ('voter', 'election')

    def __str__(self):
        return f"Vote by {self.voter.user.username} in {self.election.title}"

class VoteAuditLog(models.Model):
    voter_username = models.CharField(max_length=150)
    election_title = models.CharField(max_length=200)
    candidate_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Audit: {self.voter_username} voted in {self.election_title}"
