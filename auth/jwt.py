from authx import AuthX, AuthXConfig
from ..core.config import settings

config =AuthXConfig()
config.JWT_ALGORITHM = settings.jwt_algorithm
config.JWT_SECRET_KEY = settings.jwt_secret_key
config.JWT_ACCESS_TOKEN_EXPIRES = settings.access_expiries
config.JWT_REFRESH_TOKEN_EXPIRES = settings.refresh_expiries

security = AuthX(config=config)
