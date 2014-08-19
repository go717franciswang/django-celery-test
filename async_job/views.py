from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from async_job.forms import CreateJobForm
from async_job.models import Job
from async_job.tasks import run_job
from django.core import serializers

def index(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid():
            job = Job(total_records=form.cleaned_data['total_records'])
            job.save()
            run_job.delay(job.id)
            return HttpResponseRedirect('/progress/%d' % (job.id,))
    else:
        form = CreateJobForm()

    return render(request, 'create_job.html', {'form': form})

def progress(request, job_id):
    job = Job.objects.get(pk=job_id)
    return render(request, 'job_progress.html', {'job_id': job_id})

def progress_json(request, job_id):
    job = Job.objects.get(pk=job_id)
    data = serializers.serialize('json', [job,])
    return HttpResponse(data, content_type="application/json")

