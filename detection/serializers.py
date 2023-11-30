from rest_framework import serializers
from .models import Detection

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        ordering = ["-created_at"]
        fields = ["id", "original_image", "result_image", "created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
        }