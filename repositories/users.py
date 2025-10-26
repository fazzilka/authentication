from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User

async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
    res = await session.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def get_by_id(session: AsyncSession, user_id: UUID) -> Optional[User]:
    res = await session.execute(select(User).where(User.email == user_id))
    return res.scalar_one_or_none()

async def create(session: AsyncSession, *, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user