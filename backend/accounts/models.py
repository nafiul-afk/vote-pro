# FILE: backend/accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class Voter(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('BLOCKED', 'Blocked'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter_profile')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.status})"

    @property
    def is_blocked(self):
        return self.status == 'BLOCKED'
