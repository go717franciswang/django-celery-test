from __future__ import absolute_import

from celery import shared_task, states
from async_job.models import Job
from .celery import app as celery_app
import time
from celery.exceptions import SoftTimeLimitExceeded, MaxRetriesExceededError
from celery import group, chain

@shared_task
def run_job(job_id):
    Job.objects.get(pk=job_id).run_job()

@celery_app.task(bind=True, soft_time_limit=1, default_retry_delay=1, max_retries=2)
def long_running_job(self):
    try:
        time.sleep(10)
        return True
    except SoftTimeLimitExceeded as e:
        print 'Retrying'
        return self.retry(propagates=True) # propagating is a must

def do_long_running_job():
    r = long_running_job.delay()
    while r.state not in ('FAILURE', 'SUCCESS'):
        print "waiting..", r.state
        time.sleep(0.5)
    print r.state
    return r

@celery_app.task(bind=True, soft_time_limit=1, default_retry_delay=1, max_retries=2)
def enough_time_after_retry(self):
    try:
        time.sleep(2.5-self.request.retries)
        return "retried result"
    except SoftTimeLimitExceeded as e:
        print 'Retrying'
        return self.retry(propagates=True)

def do_enough_time_after_retry():
    r = enough_time_after_retry.delay()
    # r.wait()
    while r.state not in ('FAILURE', 'SUCCESS'):
        print "waiting..", r.state
        time.sleep(0.5)
    print r.state
    return r.get()

@celery_app.task()
def preparation_task():
    print "start preparation"
    time.sleep(1)
    print "end preparation"

@celery_app.task()
def final_task():
    print "start final task"
    time.sleep(1)
    print "end final task"

def preparations_and_final():
    g = group(preparation_task.s() for i in xrange(100))
    c = chain(g, final_task.si())
    c.apply_async()

