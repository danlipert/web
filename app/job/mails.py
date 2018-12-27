from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from marketing.mails import send_mail, setup_lang

def job_alert(job):
    to_email = settings.CONTACT_EMAIL
    from_email = settings.SERVER_EMAIL
    cur_language = translation.get_language()
    try:
        setup_lang(to_email)
        subject = _("New Job Posting Alert")
        body_str = _("A new job has been posted and is awaiting approval")
        body = f"{body_str} {job.company}:"\
            f"{settings.BASE_URL}_administrationjob/job/{job.pk}/change/"
        send_mail(
            from_email,
            to_email,
            subject,
            body,
            from_name=_("No Reply from Gitcoin.co"),
            categories=['admin'],
        )
    finally:
        translation.activate(cur_language)

def job_active_alert(job):
    to_email = job.owner_profile.email
    from_email = settings.SERVER_EMAIL
    cur_language = translation.get_language()
    try:
        setup_lang(to_email)
        subject = _("Your Gitcoin Job Posting is now active")
        body_str = _("Congratulations! Your Job Posting is now available on Gitcoin!\n")
        body = f"{body_str} {job.company}:"\
            f"{settings.BASE_URL}job/{job.pk}/{job.slug}/"
        send_mail(
            from_email,
            to_email,
            subject,
            body,
            from_name=_("No Reply from Gitcoin.co"),
            categories=[],
        )
    finally:
        translation.activate(cur_language)
