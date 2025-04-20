from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .jwt_utils import verify_token, generate_token
from .user_store import user_store
from .schemas import (
    LoginRequestSerializer, SignupRequestSerializer,
    TokenResponseSerializer, SignupResponseSerializer, ErrorResponseSerializer,
    LOGIN_REQUEST_EXAMPLE, LOGIN_SUCCESS_EXAMPLE, LOGIN_ERROR_EXAMPLE,
    SIGNUP_REQUEST_EXAMPLE, SIGNUP_SUCCESS_EXAMPLE, SIGNUP_ERROR_EXAMPLE,
    AUTH_SUCCESS_EXAMPLE, TOKEN_EXPIRED_EXAMPLE, INVALID_TOKEN_EXAMPLE, TOKEN_NOT_FOUND_EXAMPLE
)

# 회원가입
class SignupView(APIView):
    @extend_schema(
        request=SignupRequestSerializer,
        responses={
            201: OpenApiResponse(response=SignupResponseSerializer, examples=[SIGNUP_SUCCESS_EXAMPLE]),
            400: OpenApiResponse(response=ErrorResponseSerializer, examples=[SIGNUP_ERROR_EXAMPLE])
        },
        examples=[SIGNUP_REQUEST_EXAMPLE]
    )
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        nickname = data.get("nickname")

        if not username or not password or not nickname:
            return Response(
                {"error": {"code": "INVALID_INPUT", "message": "모든 필드를 입력해주세요."}},
                status=status.HTTP_400_BAD_REQUEST
            )

        success = user_store.add_user(username, password, nickname)
        if not success:
            return Response(
                {"error": {"code": "USER_ALREADY_EXISTS", "message": "이미 가입된 사용자입니다."}},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"username": username, "nickname": nickname}, status=status.HTTP_201_CREATED)

# 로그인
class LoginView(APIView):
    @extend_schema(
        request=LoginRequestSerializer,
        responses={
            200: OpenApiResponse(response=TokenResponseSerializer, examples=[LOGIN_SUCCESS_EXAMPLE]),
            400: OpenApiResponse(response=ErrorResponseSerializer, examples=[LOGIN_ERROR_EXAMPLE])
        },
        examples=[LOGIN_REQUEST_EXAMPLE]
    )
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        user = user_store.validate_credentials(username, password)
        if not user:
            return Response({
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "아이디 또는 비밀번호가 올바르지 않습니다."
                }
            }, status=400)

        token = generate_token(user)
        return Response({"token": "Bearer " + token})

# 현재 사용자 정보
class MeView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(response=TokenResponseSerializer, examples=[AUTH_SUCCESS_EXAMPLE]),
            401: OpenApiResponse(response=ErrorResponseSerializer, examples=[
                TOKEN_EXPIRED_EXAMPLE, INVALID_TOKEN_EXAMPLE, TOKEN_NOT_FOUND_EXAMPLE
            ])
        },
    )
    def get(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({
                "error": {
                    "code": "TOKEN_NOT_FOUND",
                    "message": "토큰이 없습니다."
                }
            }, status=401)

        token = auth_header.split(" ")[1]
        result = verify_token(token)

        if "error" in result:
            code = result["error"]
            message = {
                "TOKEN_EXPIRED": "토큰이 만료되었습니다.",
                "INVALID_TOKEN": "토큰이 유효하지 않습니다."
            }.get(code, "알 수 없는 인증 오류입니다.")

            return Response({
                "error": {"code": code, "message": message}
            }, status=401)

        return Response({
            "message": f"{result['username']}님 안녕하세요!",
            "user_id": result["id"]
        })