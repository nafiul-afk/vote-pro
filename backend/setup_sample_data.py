# FILE: backend/setup_sample_data.py

import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from elections.models import Election, Candidate
from django.contrib.auth.models import User
from accounts.models import Voter

def run():
    print("Creating sample data...")

    # 1. Create Presidential Election (Running)
    e1 = Election.objects.create(
        title="2026 General Presidential Election",
        description="Public vote to choose the next head of state for the upcoming 4-year term.",
        start_date=timezone.now() - datetime.timedelta(days=1),
        end_date=timezone.now() + datetime.timedelta(days=7),
        status='RUNNING'
    )
    
    Candidate.objects.create(election=e1, name="John Doe", bio="Experienced leader with focus on economy.")
    Candidate.objects.create(election=e1, name="Jane Smith", bio="Forward-thinking innovator focusing on education.")
    Candidate.objects.create(election=e1, name="Alex Johnson", bio="Independent candidate with focus on healthcare.")

    # 2. Create Tech Council Election (Upcoming)
    e2 = Election.objects.create(
        title="Regional Tech Council 2026",
        description="Community election for tech industry representatives.",
        start_date=timezone.now() + datetime.timedelta(days=10),
        end_date=timezone.now() + datetime.timedelta(days=15),
        status='UPCOMING'
    )
    
    Candidate.objects.create(election=e2, name="Sarah Connor", bio="Cybersecurity expert.")
    Candidate.objects.create(election=e2, name="Bruce Wayne", bio="Tech mogul and philanthropist.")

    # 3. Create Finished Election
    e3 = Election.objects.create(
        title="Departmental Lead Vote",
        description="Internal vote for the engineering department lead.",
        start_date=timezone.now() - datetime.timedelta(days=10),
        end_date=timezone.now() - datetime.timedelta(days=2),
        status='FINISHED'
    )
    
    Candidate.objects.create(election=e3, name="Alice Morgan", bio="Senior Architect.")
    Candidate.objects.create(election=e3, name="Bob Wilson", bio="Project Manager.")

    print("Sample data created successfully!")

if __name__ == '__main__':
    run()
