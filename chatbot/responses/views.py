from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from .models import Response
from .serializers import ResponseSerializer
class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    @action(detail=False, methods=["post"])
    def send_prompt(self, request):
        requested_prompt = request.data.get("requested_prompt")
        
        if not requested_prompt:
            return DRFResponse(
                {"error": "requested_prompt field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        
        response = Response.objects.create(user=user, prompt=requested_prompt)
        
        return DRFResponse(
            {"message": "Prompt saved successfully.", "data": {"user_id": user.id, "prompt": requested_prompt}},
            status=status.HTTP_201_CREATED
        )
