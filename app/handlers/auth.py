from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse,JWTToken
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