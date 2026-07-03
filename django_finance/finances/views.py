import time

from django.conf import settings
from rest_framework import generics, viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Category, User, Transaction
from .redis_client import redis_client
from .serializers import CategorySerializer, RegisterSerializer, TransactionSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.pop('refresh')
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                path='/auth/',
            )
        return response

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get('refresh_token')
        if raw_token is None:
            raise AuthenticationFailed('Refresh token cookie missing.')

        try:
            token = RefreshToken(raw_token)
        except TokenError as e:
            raise AuthenticationFailed(str(e))

        if redis_client.exists(f'blocklist:{token["jti"]}'):
            raise AuthenticationFailed('Token has been revoked.')

        serializer = self.get_serializer(data={'refresh': raw_token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=200)

class LogoutView(APIView):
    # AllowAny because the refresh cookie *is* the credential we're
    # checking here — not the (possibly already-expired) access token.
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get('refresh_token')
        if raw_token:
            try:
                token = RefreshToken(raw_token)
                ttl = token['exp'] - int(time.time())
                if ttl > 0:
                    redis_client.set(f'blocklist:{token["jti"]}', '1', ex=ttl)
            except TokenError:
                pass  # already invalid/expired — nothing to blocklist

        response = Response({'detail': 'Logged out.'}, status=200)
        response.delete_cookie('refresh_token', path='/auth/')
        return response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # For now, allow anyone to see/edit, but we can restrict this later
    permission_classes = [permissions.AllowAny]

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This is a best practice: only show transactions for the current user
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # This automatically sets the 'user' field to the current user when creating a new transaction
        serializer.save(user=self.request.user)