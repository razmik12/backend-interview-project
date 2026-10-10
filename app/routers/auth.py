from fastapi import APIRouter, Cookie, Depends, Request, Response, status

from app.dependencies import get_auth_service, get_current_user
from app.models.user import UserORM
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    data: UserCreate, service: AuthService = Depends(get_auth_service)
):
    return await service.register(data=data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_user(
    request: Request,
    response: Response,
    data: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    client = request.client
    ip_address = client.host if client is not None else "unknown"
    return await service.login(data=data, response=response, ip_address=ip_address)


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def profile(user: UserORM = Depends(get_current_user)):
    return user


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    response: Response,
    service: AuthService = Depends(get_auth_service),
    token: str | None = Cookie(default=None, alias="refresh_token"),
):
    return await service.refresh_access_token(refresh_token=token, response=response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    response: Response,
    token: str | None = Cookie(default=None, alias="refresh_token"),
    service: AuthService = Depends(get_auth_service),
):
    await service.logout(token=token, response=response)
