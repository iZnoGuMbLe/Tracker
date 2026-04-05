
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, JWTToken, RefreshTokenRequest, \
    ResendVerificationRequest, ResendMessageResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.repositories.user import UserRepository
from app.service.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    repository = UserRepository(session)
    return AuthService(repository)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    return await service.register(user_data)


@router.post("/login", response_model=JWTToken)
async def login(
    credentials: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    return await service.login(credentials)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.post("/refresh", response_model=JWTToken)
async def refresh(
        request: RefreshTokenRequest,
        service: AuthService = Depends(get_auth_service)
):
    return await service.refresh(request.refresh_token)

@router.get("/verify-email",response_model=JWTToken)
async def verify_user_email(
        token: str,
        service: AuthService = Depends(get_auth_service),
):
    return await service.verify_user(token)

@router.post("/resend-verification", response_model=ResendMessageResponse)
async def resend_email_verif(
        request: ResendVerificationRequest,
        service: AuthService = Depends(get_auth_service),
):
    return await service.resend_verification(request.email)

@router.post("/forgot-password",response_model=ResendMessageResponse)
async def forgot_password(
        request: ForgotPasswordRequest,
        service: AuthService = Depends(get_auth_service)
):
    return await service.forgot_password(request.email)


@router.post("/reset-password",response_model=ResendMessageResponse)
async def reset_password(
        request: ResetPasswordRequest,
        service: AuthService = Depends(get_auth_service)
):
    return await service.reset_password(request.token, request.new_password)
