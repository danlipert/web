from datetime import datetime
from unittest.mock import patch

import pytz
from dashboard.models import Profile
from job.models import Job
from test_plus.test import TestCase


class JobAlertsTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            data={},
            handle='fred',
            email='fred@localhost'
        )

    @patch('job.mails.send_mail')
    def test_new_job_alert(self, mock_send_mail):
        """Test that an alert email is sent when a job posting is created"""
        Job.objects.create(
            active=False,
            title="Test",
            description="Test",
            company="Test",
            owner_profile=self.profile,
            apply_location="test@example.com",
            expiry_date=datetime(2008, 11, 30, tzinfo=pytz.UTC),
            github_profile="http://github.com",
            location="Test"
        )
        assert mock_send_mail.call_count == 1

    @patch('job.mails.send_mail')
    def test_approve_job_alert(self, mock_send_mail):
        """Test that an alert email is sent when a job posting is approved"""
        job = Job.objects.create(
            active=False,
            title="Test",
            description="Test",
            company="Test",
            owner_profile=self.profile,
            apply_location="test@example.com",
            expiry_date=datetime(2008, 11, 30, tzinfo=pytz.UTC),
            github_profile="http://github.com",
            location="Test"
        )
        job.active = True
        job.save()
        assert mock_send_mail.call_count == 2
