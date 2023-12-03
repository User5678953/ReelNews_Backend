from django.db import models
from django.conf import settings
from django.utils import timezone


class Archive(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_articles', null=True)

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    url = models.URLField(max_length=500, blank=True, null=True)  

    def __str__(self):
        return self.title[0:50]
    
    class Meta:
        ordering = ['-published_date']
