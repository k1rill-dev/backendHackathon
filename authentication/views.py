from typing import Dict, Any

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.models import User
from authentication.serializers import UserSerializer, RotateTokenSerializer, UserRegisterSerializer


def get_tokens_for_user(user):
    refresh: Token = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def set_cookies(response: Response, data: Dict[str, Any]) -> None:
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=data["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    response.set_cookie(
        key='refresh_token',
        value=data["refresh"],
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )


@extend_schema_view(
    list=extend_schema(
        summary="Логин пользователя",
    ),
    partial_update=extend_schema(
        description="""Вход в аккаунт""",
    )
)
class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                set_cookies(response, data)
                response.data = data
                response["X-CSRFToken"] = csrf.get_token(request)
                serializer = UserSerializer(user)
                response.data = {"Success": "Login successfully", **serializer.data}
                return response
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    list=extend_schema(
        summary="Logout",
    ),
    partial_update=extend_schema(
        description="""Выход из аккаунта""",
    )
)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            refresh_token = request.COOKIES.get(
                'refresh_token')
            token = tokens.RefreshToken(refresh_token)
            token.blacklist()

            res = Response()
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            res.delete_cookie('refresh_token')
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            res["X-CSRFToken"] = None

            return res
        except:
            raise ParseError("Invalid token")


class RotateTokensView(TokenRefreshView):
    serializer_class = RotateTokenSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            set_cookies(response, response.data)
            del response.data["refresh"]
            del response.data["access"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        response.data["success"] = True
        return super().finalize_response(request, response, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список постов",
    ),
    update=extend_schema(
        summary="Изменение существующего поста",
    ),
    partial_update=extend_schema(
        description="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Cras euismod vehicula hendrerit. Integer placerat lobortis purus, molestie 
        finibus nibh gravida sed. Etiam pretium gravida velit, et rutrum nisi posuere at. 
        Proin hendrerit eros et enim placerat, in commodo lorem tristique. Donec hendrerit ultrices 
        nulla, a maximus diam consectetur id. Cras suscipit ligula vitae sem vulputate vulputate. 
        Duis enim turpis, mollis at maximus nec, tempus ac erat. Nullam at eleifend est, non lacinia erat. 
        Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
        Nulla congue condimentum arcu, id sodales dolor aliquet nec. Nullam a consequat neque.""",
    ),
    create=extend_schema(
        summary="Создание нового поста",
    ),
)
class RegisterUserView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    model = User
    permission_classes = (AllowAny,)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        return JsonResponse({
            **UserSerializer(request.user).data
        })


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse({
            'user': request.user.email
        })
