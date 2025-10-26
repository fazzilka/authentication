from fastapi import APIRouter, Depends
from ...schemas.user import UserRead
from ...auth.deps import current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=UserRead)
async def me(user = Depends(current_user)):
    return user
    
