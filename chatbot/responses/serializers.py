from rest_framework import serializers
from .models import Response
from querys.models import Query


class ResponseSerializer(serializers.ModelSerializer):
    Query = serializers.PrimaryKeyRelatedField(queryset=Query.objects.all())
    class Meta:
        model = Response
        fields = ['id', 'response', 'timestamp', 'Query']
