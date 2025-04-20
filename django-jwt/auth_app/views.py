from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .user_store import user_store

# 회원가입
class SignupView(APIView):
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
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response(
                {"error": {"code": "INVALID_INPUT", "message": "아이디와 비밀번호를 입력해주세요."}},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = user_store.validate_credentials(username, password)
        if not user_data:
            return Response(
                {"error": {"code": "INVALID_CREDENTIALS", "message": "아이디 또는 비밀번호가 올바르지 않습니다."}},
                status=status.HTTP_401_UNAUTHORIZED
            )

        DummyUser = type("User", (), {"id": user_data["id"], "username": username})
        token = RefreshToken.for_user(DummyUser)
        return Response({"token": str(token.access_token)})
