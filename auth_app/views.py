from rest_framework import generics, permissions
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response()
        response.data = {"message": "Logged out successfully"}
        return response