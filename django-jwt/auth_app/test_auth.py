import pytest
from rest_framework.test import APIClient
from auth_app.user_store import user_store

client = APIClient()

@pytest.fixture(autouse=True)
def clear_user_store():
    # 각 테스트 전 클라이언트 초기화
    user_store.users.clear()
    client.credentials()

# 회원가입_성공
def test_signup_success():
    res = client.post("/signup", {
        "username": "testuser",
        "password": "pass1234",
        "nickname": "tester"
    }, format="json")

    assert res.status_code == 201
    assert res.data["username"] == "testuser"

# 회원가입_이미 존재하는 유저 예외
def test_signup_duplicate():
    client.post("/signup", {
        "username": "testuser",
        "password": "pass1234",
        "nickname": "tester"
    }, format="json")

    res = client.post("/signup", {
        "username": "testuser",
        "password": "pass1234",
        "nickname": "tester"
    }, format="json")

    assert res.status_code == 400
    assert res.data["error"]["code"] == "USER_ALREADY_EXISTS"

# 로그인_성공
def test_login_success():
    client.post("/signup", {
        "username": "testuser",
        "password": "pass1234",
        "nickname": "tester"
    }, format="json")

    res = client.post("/login", {
        "username": "testuser",
        "password": "pass1234"
    }, format="json")

    assert res.status_code == 200
    assert "token" in res.data

# 로그인_인증 실패 예외
def test_login_invalid_credentials():
    res = client.post("/login", {
        "username": "notexist",
        "password": "wrongpass"
    }, format="json")

    assert res.status_code == 401
    assert res.data["error"]["code"] == "INVALID_CREDENTIALS"

# 내 정보 가져오기_성공
def test_me_success():
    client.post("/signup", {
        "username": "testuser",
        "password": "pass1234",
        "nickname": "tester"
    }, format="json")

    login_res = client.post("/login", {
        "username": "testuser",
        "password": "pass1234"
    }, format="json")

    token = login_res.data["token"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    res = client.get("/me")

    assert res.status_code == 200
    assert res.data["user_id"] == 1
    assert "안녕하세요" in res.data["message"]

# 내 정보 가져오기_ 토큰 없을 때
def test_me_without_token():
    res = client.get("/me")
    assert res.status_code == 401
    assert res.data["error"]["code"] == "TOKEN_NOT_FOUND"
