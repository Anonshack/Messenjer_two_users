from datetime import datetime, timedelta
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from .serializers import UserRegSerializer, UserSerializer, UsersListSerializer

from .filters import UsersFilterBackend


# Create your views here.
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username, is_active=True).first()

        if user is None:
            raise AuthenticationFailed('Login yoki parol xato, iltimos tekshirib qaytadan kiriting')

        if not user.check_password(password):
            raise AuthenticationFailed('Login yoki parol xato, iltimos tekshirib qaytadan kiriting')

        payload = {
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.data = {
            'token': token
        }

        return response


class UserDetailView(APIView):
    def get(self, request):
        try:
            token = request.META['HTTP_TOKEN']
        except:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

        if not token:
            raise AuthenticationFailed('Token yaroqsiz, iltimos tizimga qayta kiring')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Sessiya muddati o\'tgan, iltimos, qayta kiring')
        except:
            raise AuthenticationFailed('Sessiya muddati o\'tgan, iltimos, qayta kiring')

        user = User.objects.filter(username=payload['username']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UsersListView(ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all()
    filter_backends = (UsersFilterBackend,)
    # def get_queryset(self):
    #     try:
    #         key_word = self.request.META['']
    #     if


def checkUserToken(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        return False

    user = User.objects.filter(username=payload['username']).first()

    if user:
        return user

    return False