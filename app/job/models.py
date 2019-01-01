from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField

from lxml.html.clean import Cleaner
from lxml import html

from economy.models import SuperModel
from .mails import job_alert, job_active_alert


class JobQuerySet(models.QuerySet):
    """Define the Job default queryset and manager."""

    def active(self):
        """Filter results down to active jobs only."""
        return self.filter(active=True)


class Job(SuperModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    owner_profile =  models.ForeignKey(
        'dashboard.Profile', null=True, on_delete=models.SET_NULL, related_name='jobs', blank=True
    )
    active = models.BooleanField(default=False)
    skills = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    company = models.CharField(max_length=255)
    github_profile = models.CharField(max_length=255, default='', blank=True)
    expiry_date = models.DateTimeField()
    apply_location = models.CharField(max_length=400)
    amount = models.DecimalField(default=1, decimal_places=4, max_digits=50)
    paid_txid = models.CharField(max_length=255, default='', blank=True)
    slug = AutoSlugField(populate_from='title')
    full_time = models.BooleanField(default=True)
    internship = models.BooleanField(default=False)
    contractor = models.BooleanField(default=False)
    annual_pay = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, default='', blank=True)

    objects = JobQuerySet.as_manager()


@receiver(post_save, sender=Job)
def alert_new_job(sender, **kwargs):
    """Alert when a new Job is created."""
    if(kwargs.get('created') is True):
        job_alert(kwargs.get('instance'))
    elif(kwargs.get('instance').active is True):
        job_active_alert(kwargs.get('instance'))


# This is not foolproof - the best thing to do is make sure all template tags
# are properly coded and no content is loaded dynamically via JS
cleaner = Cleaner(allow_tags=[''], javascript=True, style=True, remove_unknown_tags=False)

def clean_field(field):
    if not field.isspace():
        return html.fromstring(cleaner.clean_html(field)).text_content()

@receiver(pre_save, sender=Job)
def clean_job_fields(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.title = clean_field(instance.title)
    instance.company = clean_field(instance.company)
    instance.description = clean_field(instance.description)
    instance.github_profile = clean_field(instance.github_profile)
    instance.apply_location = clean_field(instance.apply_location)
    instance.location = clean_field(instance.location)
    instance.skills = [clean_field(s) for s in instance.skills]