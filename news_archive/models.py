from django.db import models

class NewsArchive(models.Model):
    source_id = models.CharField(max_length=100, null=True, blank=True)
    source_name = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=500)
    url_to_image = models.URLField(max_length=500, null=True, blank=True)
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

