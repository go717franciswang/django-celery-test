from django import forms
from async_job.models import Job, FileSaveRetrieve

class CreateJobForm(forms.Form):
    total_records = forms.IntegerField(label="Total Records")

class UploadForm(forms.ModelForm):
    class Meta:
        model = FileSaveRetrieve
        fields = ['input_file']
