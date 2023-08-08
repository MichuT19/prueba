from django.db import models

class task(models.Model):
    title = models.CharField(max_length=100)
