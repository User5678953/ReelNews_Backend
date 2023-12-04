from rest_framework.serializers import ModelSerializer
from .models import NewsArchive

class ArchiveSerializer(ModelSerializer):
    class Meta:
        model = NewsArchive
        fields = '__all__'