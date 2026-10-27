from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from app.config import get_settings
from app.db import get_db
from app.models import User
s=get_settings(); pwd=CryptContext(schemes=["bcrypt"],deprecated="auto"); oauth=OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def hash_password(v): return pwd.hash(v)
def verify_password(v,h): return pwd.verify(v,h)
def token_for(uid): return jwt.encode({"sub":uid,"exp":datetime.now(timezone.utc)+timedelta(minutes=s.access_token_expire_minutes)},s.jwt_secret,algorithm=s.jwt_algorithm)
async def current_user(token=Depends(oauth),db=Depends(get_db)):
 try: uid=jwt.decode(token,s.jwt_secret,algorithms=[s.jwt_algorithm]).get("sub")
 except JWTError: raise HTTPException(401,"Invalid authentication credentials")
 u=(await db.execute(select(User).where(User.id==uid))).scalar_one_or_none()
 if not u: raise HTTPException(401,"User not found")
 return u
