from __future__ import absolute_import

from celery import shared_task
from async_job.models import Job


@shared_task
def run_job(job_id):
    Job.objects.get(pk=job_id).run_job()
