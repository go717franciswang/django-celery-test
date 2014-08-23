from __future__ import absolute_import

from celery import shared_task, states
from async_job.models import Job
from .celery import app as celery_app
import time
from celery.exceptions import SoftTimeLimitExceeded, MaxRetriesExceededError

@shared_task
def run_job(job_id):
    Job.objects.get(pk=job_id).run_job()

@celery_app.task(bind=True, time_limit=2, soft_time_limit=1, default_retry_delay=1, max_retries=2)
def long_running_job(self):
    try:
        time.sleep(10)
        return True
    except SoftTimeLimitExceeded as e:
        print 'Retrying'
        # self.update_state(state=states.RETRY)
        return self.retry(exc=Exception('Timeout'), propagates=True)

def do_long_running_job():
    r = long_running_job.delay()
    while r.state not in ('FAILURE', 'SUCCESS'):
        print "waiting..", r.state
        time.sleep(0.5)
    return r

