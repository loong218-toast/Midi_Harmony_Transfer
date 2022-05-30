from rest_framework import serializers
from .models import midi_data

class firstappSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
    read_only=True,
    default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = midi_data
        fields = ('user', 'description', 'completed')