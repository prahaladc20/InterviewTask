from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# Create your views here.

class AuthenticateApi(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = Task2UserSerializer
    exclude_from_schema = True
    http_method_names = ['post', 'get', ]

    def create(self, request):
        try:
            data = self.request.data
            username = data.get('username')
            password = data.get('password')

            if TaskUSer.objects.filter(username=username).count() > 0:
                user = TaskUSer.objects.get(username=username)
                if not user.validiate_password(password):
                    return Response({'message': 'Passwords not Match'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'message': 'Passwords Match'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
