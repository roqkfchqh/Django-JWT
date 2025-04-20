from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample

# ===== 요청 시리얼라이저 =====
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignupRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    nickname = serializers.CharField()


# ===== 응답 시리얼라이저 =====
class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()

class SignupResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    nickname = serializers.CharField()

class ErrorDetailSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = ErrorDetailSerializer()


# ===== 예시 정의 =====
LOGIN_REQUEST_EXAMPLE = OpenApiExample(
    name="로그인 요청",
    value={"username": "CHAE YOUNG", "password": "12341234"},
    request_only=True,
)

LOGIN_SUCCESS_EXAMPLE = OpenApiExample(
    name="로그인 성공 응답",
    value={"token": "Bearer eKDIkdfjoakIdkfjpekdkcjdkoIOdjOKJDFOlLDKFJKL"},
    response_only=True,
    status_codes=["200"]
)

LOGIN_ERROR_EXAMPLE = OpenApiExample(
    name="아이디, 비밀번호 불일치",
    value={"error": {"code": "INVALID_CREDENTIALS", "message": "아이디 또는 비밀번호가 올바르지 않습니다."}},
    response_only=True,
    status_codes=["400"]
)

SIGNUP_REQUEST_EXAMPLE = OpenApiExample(
    name="회원가입 요청",
    value={"username": "CHAE YOUNG", "password": "12341234", "nickname": "lcy"},
    request_only=True
)

SIGNUP_SUCCESS_EXAMPLE = OpenApiExample(
    name="회원가입 성공 응답",
    value={"username": "CHAE YOUNG", "nickname": "lcy"},
    response_only=True,
    status_codes=["201"]
)

SIGNUP_ERROR_EXAMPLE = OpenApiExample(
    name="username 중복 예외",
    value={"error": {"code": "USER_ALREADY_EXISTS", "message": "이미 가입된 사용자입니다."}},
    response_only=True,
    status_codes=["400"]
)

AUTH_SUCCESS_EXAMPLE = OpenApiExample(
    name="인증 성공 응답",
    value={"message": "CHAE YOUNG님 안녕하세요!", "user_id": 1},
    response_only=True,
    status_codes=["200"]
)

TOKEN_EXPIRED_EXAMPLE = OpenApiExample(
    name="만료된 토큰",
    value={"error": {"code": "TOKEN_EXPIRED", "message": "토큰이 만료되었습니다."}},
    response_only=True,
    status_codes=["401"]
)

INVALID_TOKEN_EXAMPLE = OpenApiExample(
    name="유효하지 않은 토큰",
    value={"error": {"code": "INVALID_TOKEN", "message": "토큰이 유효하지 않습니다."}},
    response_only=True,
    status_codes=["401"]
)

TOKEN_NOT_FOUND_EXAMPLE = OpenApiExample(
    name="토큰 없음",
    value={"error": {"code": "TOKEN_NOT_FOUND", "message": "토큰이 없습니다."}},
    response_only=True,
    status_codes=["401"]
)