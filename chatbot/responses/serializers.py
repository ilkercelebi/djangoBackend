from rest_framework import serializers
from .models import Response
from users.models import User


class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Response
        fields = ['id', 'user', 'request_prompt', 'response', 'timestamp']
