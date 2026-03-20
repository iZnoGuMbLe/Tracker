from datetime import timedelta
from fastapi import HTTPException, status
from jose import JWTError

from app.broker.producer import producer
from app.schemas.user_schema import UserLogin, UserCreate, UserResponse, JWTToken, TokenData
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token, \
    create_verification_token, decode_verification_token
from app.core.config import settings
from app.repositories import UserRepository

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

        email_verification_token = create_verification_token(
            data={"sub": str(user.id)},
        )

        await producer.publish_message(
            queue_name= "mail_queue",
            message_body=
            {
                "type": "verification",
                "email": user.email,
                "username": user.username,
                "token": email_verification_token
            }
        )

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
        refresh_token = create_refresh_token(
            data={'sub': str(user.id)}
        )


        return JWTToken(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token:str) -> JWTToken|None:
        payload = decode_refresh_token(refresh_token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = int(payload['sub'])


        user = await self.repository.get_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect user id",
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
        refresh_token = create_refresh_token(
            data={'sub': str(user.id)}
        )

        return JWTToken(access_token=access_token,refresh_token=refresh_token)


    async def verify_user(self,verification_token:str) -> JWTToken:
        payload = decode_verification_token(verification_token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email verification token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = int(payload['sub'])

        user = await self.repository.get_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect user id",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not active"
            )

        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )

        await self.repository.verify_user(user_id)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={'sub': str(user.id)}
        )

        return JWTToken(access_token=access_token,refresh_token=refresh_token)














