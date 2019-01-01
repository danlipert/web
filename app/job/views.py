import datetime
import logging
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .models import Job

logger = logging.getLogger(__name__)


DATE_MAP = {'24_hours': datetime.timedelta(days = 1),
            '3_days': datetime.timedelta(days = 3),
            '7_days': datetime.timedelta(days = 7),
            '30_days': datetime.timedelta(days = 30)}

JOB_FILTERS = ['annual_pay', 'full_time', 'internship', 'contractor', 'date_posted', 'sort']

PAGE_LIMIT = 25

AVAILABLE_SKILLS = json.dumps([
    "ActionScript",
    "AppleScript",
    "Asp",
    "BASIC",
    "C",
    "C++",
    "Clojure",
    "COBOL",
    "ColdFusion",
    "Erlang",
    "Fortran",
    "Go",
    "Groovy",
    "Haskell",
    "Java",
    "JavaScript",
    "Lisp",
    "Perl",
    "PHP",
    "Python",
    "Ruby",
    "Rust",
    "Scala",
    "Scheme",
    "Solidity"])


def jobs(request):
    limit = request.GET.get('limit', PAGE_LIMIT)
    page = request.GET.get('page', 1)
    sort = request.GET.get('sort_option', '-created_on')
    date_posted = request.GET.get('date_posted', '30_days')
    annual_pay = request.GET.get('annual_pay', "Any")

    if any([p in request.GET for p in ['full_time', 'part_time', 'contractor', 'internship']]):
        job_type_default = False
    else:
        job_type_default = True

    full_time = request.GET.get('full_time', job_type_default)
    part_time = request.GET.get('part_time', job_type_default)
    contractor = request.GET.get('contractor', job_type_default)
    internship = request.GET.get('internship', job_type_default)

    search = request.GET.get('search', '')

    filters = {'created_on__gt': datetime.datetime.now() - DATE_MAP[date_posted],
               'expiry_date__gt': datetime.datetime.now()}

    if annual_pay != "Any":
        filters['annual_pay__gt'] = int(annual_pay)

    if full_time and not part_time:
        filters['full_time'] = True
    if part_time and not full_time:
        filters['full_time'] = False

    if not contractor:
        filters['contractor'] = False
    if not internship:
        filters['internship'] = False

    if search:
        filters['skills__icontains'] = search

    _jobs = Job.objects.select_related('owner_profile').active().filter(**filters).order_by(sort)

    paginator = Paginator(_jobs, limit)
    jobs = paginator.get_page(page)

    params = {
        'active': 'jobs_landing',
        'title': _('Jobs Explorer'),
        'jobs': jobs,
        'jobs_count': _jobs.count(),
        'date_posted': date_posted,
        'filters': {f:request.GET.get(f) for f in JOB_FILTERS},
        'annual_pay': annual_pay,
        'full_time': full_time,
        'part_time': part_time,
        'contractor': contractor,
        'internship': internship,
        'search': search,
        'page_limit': PAGE_LIMIT
    }
    return TemplateResponse(request, 'job/index.html', params)


@csrf_exempt
def job_details(request, job_id, job_slug):
    """Display the Job details page."""

    try:
        job = Job.objects.get(pk=job_id, slug=job_slug)
    except Job.DoesNotExist:
        raise Http404

    params = {
        'active': 'jobs_detail',
        'job': job,
        'title': job.title,
        'description': job.description,
        'company': job.company,
        'experience': job.skills,
        'created': job.created_on,
        'owner_profile_email': job.owner_profile.email,
        'owner_profile_handle': job.owner_profile.handle
    }
    return TemplateResponse(request, 'job/detail.html', params)


@login_required
def job_new(request):
    profile = request.user.profile if request.user.is_authenticated and request.user.profile else None

    if request.method == 'POST':

        job_kwargs = {
            'title': request.POST.get('title', ''),
            'description': request.POST.get('description', ''),
            'skills': request.POST.get('skills', '').split(','),
            'company': request.POST.get('company', ''),
            'github_profile': request.POST.get('github_profile', ''),
            'apply_location': request.POST.get('apply_location', ''),
            'expiry_date': datetime.datetime.now() + datetime.timedelta(days=30),
            'owner_profile': profile,
            'paid_txid': request.POST.get('paid_txid'),
            'full_time': True if request.POST.get('full_time') else False,
            'internship': True if request.POST.get('internship') else False,
            'contractor': True if request.POST.get('contractor') else False,
            'annual_pay': request.POST.get('annual_pay'),
            'location': request.POST.get('location')
        }

        # fix autocomplete js
        if job_kwargs['skills'][-1].isspace():
            job_kwargs['skills'].pop()

        job = Job.objects.create(**job_kwargs)

        return redirect(reverse('job:details', args=(job.pk, job.slug)))

    params = {
        'github_profile': profile.github_url,
        'job_posting_eth_fee': settings.JOB_POSTING_ETH_FEE,
        'job_posting_eth_address': settings.JOB_POSTING_ETH_ADDRESS,
        'available_skills': AVAILABLE_SKILLS
    }

    return TemplateResponse(request, 'job/new.html', params)
