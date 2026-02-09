from datetime import timedelta
from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user_schema import UserLogin,UserCreate,UserResponse,JWTToken
from app.core.security import verify_password, create_access_token
from app.core.config import settings

class AuthService:
    def __init__(self, repository:UserRepository):
        self.repository = repository

    async def register(self, user_data: UserCreate) -> UserResponse:

        existing_user = await self.repository.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        existing_email = await self.repository.get_user_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = await self.repository.create_user(user_data)
        return UserResponse.model_validate(user)


    async def login(self, credentials: UserLogin) -> JWTToken:
        user = await self.repository.get_user_by_username(credentials.username)

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not active"
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return JWTToken(access_token=access_token)



