from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from .models import Query
from .serializers import QuerySerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail = False,methods=["post"])
    def send_query(self,request):
        user = request.user
        prompt = request.data.get("user_query")
        if not prompt:
            return DRFResponse(
                {"error": "requested_prompt field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        query = Query.objects.create(user=user,user_query=prompt)
        return DRFResponse(
            {"message": "Prompt saved successfully.", "data": {"user_id": user.id, "prompt": prompt, "query_id": query.id}},
            status=status.HTTP_201_CREATED
        )