from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]  

    @action(detail=False, methods=["get"])
    def list_users(self, request):
        users = self.queryset.filter(is_active=True)  
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def create_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=True)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login_user(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Kullanıcı adı veya şifre eksik"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Kullanıcı adı veya şifre hatalı"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_recaptcha(self, request):
        # Frontend'den gelen token'ı alın
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Google reCAPTCHA doğrulama endpointi
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,  # Secret Key
            'response': token,
        }

        # Google API'ye istek gönder
        response = requests.post(url, data=data)
        result = response.json()

        # Yanıtı kontrol et
        if result.get('success'):
            return Response({'success': True, 'score': result.get('score', 0)}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': result.get('error-codes')}, status=status.HTTP_400_BAD_REQUEST)

        
