from datetime import datetime

import pytz
from job.models import Job
from test_plus.test import TestCase


class ScriptInjectionTest(TestCase):

    def test_prevent_script_injection(self):
        """Test that a job posting cannot contain a script injection attack"""
        job = Job.objects.create(
            active=False,
            title="Test",
            company="Test",
            apply_location="test@example.com",
            description="Lorem Ipsum <script>alert(':O');</script>Lorem Ipsum",
            expiry_date=datetime(2008, 11, 30, tzinfo=pytz.UTC),
            github_profile="http://github.com",
            location="Test"
        )
        assert job.description == "Lorem Ipsum Lorem Ipsum"
