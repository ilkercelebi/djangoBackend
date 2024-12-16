from rest_framework import serializers
from .models import Query
from users.models import User


class QuerySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Query
        fields = ['id', 'user_query', 'user','timestamp']
