from django.db import models
from django.contrib.auth.models import User

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

class TotalTime(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    time = models.ForeignKey(TimeEntry, on_delete=models.CASCADE)
