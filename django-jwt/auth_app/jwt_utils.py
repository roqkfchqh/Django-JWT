import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_token(user_data):
    payload = {
        "id": user_data["id"],
        "username": user_data["username"],
        "exp": datetime.now() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "TOKEN_EXPIRED"}
    except jwt.InvalidTokenError:
        return {"error": "INVALID_TOKEN"}
