from django.db import models
from django.conf import settings

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_documents', blank=True)

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
