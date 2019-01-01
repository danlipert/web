# -*- coding: utf-8 -*-
"""Handle job URLs.

Copyright (C) 2018 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
from django.urls import path, re_path

from job.views import (
    job_details, job_new, jobs
)

app_name = 'job'
urlpatterns = [
    path('', jobs, name='jobs'),
    path('<int:job_id>/<slug:job_slug>', job_details, name='details'),
    re_path(r'^new', job_new, name='new'),
]