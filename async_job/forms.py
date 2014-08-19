from django import forms
from async_job.models import Job

class CreateJobForm(forms.Form):
    total_records = forms.IntegerField(label="Total Records")
