from django.db import models
from django.conf import settings



class Blog(models.Model):
    title = models.JSONField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
