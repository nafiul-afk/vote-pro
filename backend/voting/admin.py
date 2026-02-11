# FILE: backend/voting/admin.py
from django.contrib import admin
from .models import Vote, VoteAuditLog

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'election', 'candidate', 'timestamp')
    list_filter = ('election', 'candidate')

@admin.register(VoteAuditLog)
class VoteAuditLogAdmin(admin.ModelAdmin):
    list_display = ('voter_username', 'election_title', 'candidate_name', 'timestamp', 'ip_address')
    readonly_fields = ('voter_username', 'election_title', 'candidate_name', 'timestamp', 'ip_address')
