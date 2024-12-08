from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Response
from .serializers import ResponseSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
