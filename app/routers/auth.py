from app.dependencies import get_auth_service, get_current_user
from fastapi import APIRouter, Depends, status
from app.models.user import UserORM
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])
    

@router.post("/register",response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def register_user(data:UserCreate,service:AuthService = Depends(get_auth_service)):
    return await service.register(data=data)


@router.post("/login",response_model=TokenResponse,status_code=status.HTTP_200_OK)
async def login_user(data:UserLogin,service:AuthService = Depends(get_auth_service)):
    return await service.login(data=data)


@router.get("/me",response_model=UserOut,status_code=status.HTTP_200_OK)
async def profile(user:UserORM = Depends(get_current_user)):
    return user