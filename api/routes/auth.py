from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from authx import TokenPayload

from ...core.security import hash_password, verify_password
from ...db.session import get_session
from ...repositories import users as users_repo
from ...schemas.auth import RegisterIn, LoginIn, TokenPair
from ...schemas.user import UserRead
from ...auth.jwt import security

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterIn, session: AsyncSession = Depends(get_session)):
    existing = await users_repo.get_by_email(session, data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = await users_repo.create(
        session,
        email=data.email,
        hashed_password=hash_password(data.password.get_secret_value()),
    )
    return user

@router.post("/login", response_model=TokenPair)
async def login(data: LoginIn, session: AsyncSession = Depends(get_session)):
    user = await users_repo.get_by_email(session, data.email)
    if not user or not verify_password(data.password.get_secret_value(), user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access =security.create_access_token(uid=str(user.id))
    refresh = security.create_refresh_token(uid=str(user.id))
    return TokenPair(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=dict)

async def refresh(payload: TokenPayload = Depends(security.refresh_token_required)):
    # созаём новый access по refresh (uid берём из sub)
    new_access = security.create_access_token(uid=payload.sub)
    return {"access_token": new_access, "token_type": "baerer"}
