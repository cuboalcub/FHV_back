import jwt
import datetime
from django.conf import settings

class JWTService:
    SECRET_KEY = settings.SECRET_KEY  
    
    @staticmethod
    def generate_token(user_id):
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
            "iat": datetime.datetime.now(datetime.timezone.utc)
        }
        return jwt.encode(payload, JWTService.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, JWTService.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
