from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.
class RegisterAPIView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    exclude_from_schema = True
    http_method_names = ['post', 'get', ]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework import authentication
# from rest_framework import exceptions


# class ExampleAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         # username = request.META.get('HTTP_X_USERNAME')
#         username = request.GET.get('username')
#         if not username:
#             return None
#
#         try:
#             user = TaskUSer.objects.get(username=username)
#         except TaskUSer.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')
#         return (user, None)


class UserAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer
    exclude_from_schema = True
    http_method_names = ['get', ]

    def get_queryset(self):
        self.queryset = self.request.user
        return self.queryset

    def retrieve(self, request, pk=None):
        data = {}
        return Response(data, status=status.HTTP_200_OK)


class LoginAPIView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    exclude_from_schema = True
    http_method_names = ['post', 'get', ]

    def create(self, request):
        data = self.request.data
        username = data.get('username')
        password = data.get('password')

        if TaskUSer.objects.filter(username=username).count() > 0:
            user = TaskUSer.objects.get(username=username)
            if not user.validiate_password(password):
                raise ValueError("Invalidate user")

            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user, context={'request': request}).data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'query_status': 'successful', 'user': user_data
            })