# from django.shortcuts import get_object_or_404
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response as DRFResponse
# from .models import Response
# from .serializers import ResponseSerializer
# from .models import Query
# from .llama import generate_response  # Model fonksiyonunu ekledik
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class ResponseViewSet(viewsets.ModelViewSet):
#     queryset = Response.objects.all()
#     serializer_class = ResponseSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=["post"])
#     def process_response(self, request):
#         """
#         Kullanıcının daha önce kaydettiği bir sorguyu alır ve modeli çalıştırarak yanıt döndürür.
#         """
#         query_id = request.data.get("query_id")
#         if not query_id:
#             return DRFResponse(
#                 {"error": "query_id field is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         query = get_object_or_404(Query, id=query_id)

#         try:
#             output_text = generate_response(query.user_query)
#         except Exception as e:
#             return DRFResponse(
#                 {"error": f"Model çalıştırılırken hata oluştu: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         response = Response.objects.create(
#             user=request.user,
#             query=query,
#             result=output_text
#         )


#         return DRFResponse(
#             {
#                 "message": "Yanıt başarıyla oluşturuldu.",
#                 "data": {
#                     "response_id": response.id,
#                     "query": query.user_query,
#                     "result": output_text,
#                 },
#             },
#             status=status.HTTP_201_CREATED
#         )

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse  # Rename DRF Response
from .models import Response as ResponseModel  # Rename model import to ResponseModel
from .serializers import ResponseSerializer
from .models import Query
from .llama import generate_response  # Model fonksiyonunu ekledik
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()  # Use ResponseModel here
    serializer_class = ResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def process_response(self, request):
        """
        Kullanıcının daha önce kaydettiği bir sorguyu alır ve modeli çalıştırarak yanıt döndürür.
        """
        query_id = request.data.get("query_id")
        if not query_id:
            return DRFResponse(
                {"error": "query_id field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        query = get_object_or_404(Query, id=query_id)

        try:
            output_text = generate_response(query.user_query)
        except Exception as e:
            return DRFResponse(
                {"error": f"Model çalıştırılırken hata oluştu: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Use ResponseModel instead of Response
        response = ResponseModel.objects.create(
            user=request.user,
            query=query,
            result=output_text
        )

        return DRFResponse(
            {
                "message": "Yanıt başarıyla oluşturuldu.",
                "data": {
                    "response_id": response.id,
                    "query": query.user_query,
                    "result": output_text,
                },
            },
            status=status.HTTP_201_CREATED
        )
