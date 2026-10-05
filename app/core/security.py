import hashlib
import uuid
from jose import jwt,JWTError
from datetime import timedelta,timezone,datetime
from app.config import settings
from app.exceptions.user_exception import InvalidCredentialsError
from pwdlib import PasswordHash
from app.schemas.user import RefreshPayload

config_hash = PasswordHash.recommended()

def hash_password(password:str)->str:
    return config_hash.hash(password)

def verify_password(password: str, hashed_password: str)->bool:
    return config_hash.verify(password,hashed_password)



def create_access_token(user_id:uuid.UUID)->str:
    time_life = datetime.now(timezone.utc) + timedelta(minutes=settings.access_exp)
    payload = {
        "sub":str(user_id),
        "exp":time_life,
        "type":"access_token",
    }
    token = jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return token



def create_refresh_token(user_id:uuid.UUID,session_id:uuid.UUID)->str:
    time_life = datetime.now(timezone.utc) + timedelta(days=settings.refresh_exp)
    payload = {
        "sub":str(user_id),
        "exp":time_life,
        "jti": str(uuid.uuid4()),
        "type":"refresh_token",
        "session_id":str(session_id)
    }
    token = jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return token


def decode_access_token(token:str)->uuid.UUID:
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        
        if  payload.get("type") != "access_token":
                    raise InvalidCredentialsError()
        user_id = payload.get(str("sub"))     
        
        if not user_id:
            raise InvalidCredentialsError()
        return uuid.UUID(user_id)
    except (JWTError,ValueError):
        raise InvalidCredentialsError()
    

def decode_refresh_token(token: str) -> RefreshPayload:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        if payload.get("type") != "refresh_token":
            raise InvalidCredentialsError()

        if not payload.get("sub"):
            raise InvalidCredentialsError()

        if not payload.get("session_id"):
            raise InvalidCredentialsError()

        return RefreshPayload(
            sub=payload.get("sub"),
            session_id=uuid.UUID(payload["session_id"]),
        )

    except (JWTError, ValueError):
        raise InvalidCredentialsError()
    


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
