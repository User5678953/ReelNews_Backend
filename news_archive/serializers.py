from rest_framework.serializers import ModelSerializer
from .models import Archive

class ArchiveSerializer(ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'