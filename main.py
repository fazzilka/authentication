from fastapi import FastAPI
from .core.config import settings
from .db.session import engine
from .db.base import Base

from .api.routes.auth import router as auth_router
from .api.routes.users import router as users_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.app_debag)

    #Роуты
    app.include_router(auth_router)
    app.include_router(users_router)

    # Создание таблиц на старте (для dev; в prod в будущем будет миграция через Alembic)
    @app.on_event("startup")
    async def on_startup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app

app = create_app()
