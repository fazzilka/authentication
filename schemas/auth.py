from pydantic import BaseModel, EmailStr, SecretStr

class RegisterIn(BaseModel):
    email: EmailStr
    password: SecretStr

class LoginIn(BaseModel):
    email: EmailStr
    password: SecretStr

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"