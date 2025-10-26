from pwdlib import PasswordHash

pwd_ctx = PasswordHash.recommended()

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def verify_password(plain:str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)