import time
from django.db import models

class Job(models.Model):
    total_records = models.IntegerField()
    processed_records = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def run_job(self):
        while self.processed_records < self.total_records:
            time.sleep(1)
            self.processed_records += 1
            self.save()

    def __unicode__(self):
        return "%d, %d / %d" % (self.id, self.processed_records, self.total_records)

class FileSaveRetrieve(models.Model):
    input_file = models.FileField(upload_to='input')
    output_file = models.FilePathField(null=True)

    def __unicode__(self):
        return self.input_file.url()
