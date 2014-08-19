from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from async_job.forms import CreateJobForm, UploadForm
from async_job.models import Job, FileSaveRetrieve
from async_job.tasks import run_job
from django.core import serializers
from django.conf import settings
from django.db import models
import os

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

def file_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # instead of .save(commit=False) because .url later won't be correctly generated
            fileupload = form.save() 
            fileupload.output_file = fileupload.input_file.url
            fileupload.save()
            return HttpResponseRedirect('/success/%d' % (fileupload.id,))
    else:
        form = UploadForm()

    return render(request, 'file_upload.html', {'form': form})

def success(request, fileupload_id):
    x = FileSaveRetrieve.objects.get(pk=fileupload_id)
    url = os.path.join(settings.MEDIA_URL, x.input_file.url)
    return HttpResponse('<a href="%s">%s</a>' % (url, url))
