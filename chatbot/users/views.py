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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]  # Herkese erişim izni tanımlı

    @action(detail=False, methods=["get"])
    def list_users(self, request):
        users = self.queryset.filter(is_active=True)  # Sadece aktif kullanıcıları listele
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

        # Kullanıcı doğrulama
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            # Kullanıcı giriş işlemlerini JWT ile gerçekleştir
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Kullanıcı adı veya şifre hatalı"},
            status=status.HTTP_401_UNAUTHORIZED
        )
