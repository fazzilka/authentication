from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from authx import TokenPayload

from ..db.session import get_session
from ..repositories.users import get_by_id
from .jwt import security

async def current_user(
        payload: TokenPayload = Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session),
):
    #sub хранит UUID
    try:
        user_id = UUID(payload.sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    user = await get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
        
