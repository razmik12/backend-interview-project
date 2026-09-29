import uuid

from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import timedelta,timezone,datetime
from app.config import settings
from app.exceptions.user_exception import UserNotFoundError,InvalidCredentialsError
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str)->bool:
    return pwd_context.verify(password,hashed_password)



def create_access_token(user_id:uuid.UUID)->str:
    time_life = datetime.now(timezone.utc) + timedelta(minutes=settings.access_exp)
    payload = {
        "sub":str(user_id),
        "exp":time_life,
        "type":"access_token",
    }
    token = jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return token



def create_refresh_token(user_id:uuid.UUID)->str:
    time_life = datetime.now(timezone.utc) + timedelta(days=settings.refresh_exp)
    payload = {
        "sub":str(user_id),
        "exp":time_life,
        "type":"refresh_token",
    }
    token = jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return token


def decode_access_token(token)->uuid.UUID:
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        
        if  payload.get("type") != "access_token":
                    raise InvalidCredentialsError()
        user_id = payload.get(str("sub"))     
        
        if not user_id:
            raise InvalidCredentialsError()
        return uuid.UUID(user_id)
    except JWTError:
        raise InvalidCredentialsError()
    
        
