from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.db import get_db
from app.models import User
from app.schemas.models import RegisterRequest,TokenResponse
from app.security import hash_password,verify_password,token_for,current_user
router=APIRouter(prefix="/auth")
@router.post("/register")
async def register(b:RegisterRequest,db=Depends(get_db)):
 if (await db.execute(select(User).where(User.email==b.email))).scalar_one_or_none(): raise HTTPException(409,"Email already registered")
 u=User(email=b.email,hashed_password=hash_password(b.password)); db.add(u); await db.commit(); await db.refresh(u); return {"id":u.id,"email":u.email}
@router.post("/login",response_model=TokenResponse)
async def login(f:OAuth2PasswordRequestForm=Depends(),db=Depends(get_db)):
 u=(await db.execute(select(User).where(User.email==f.username))).scalar_one_or_none()
 if not u or not verify_password(f.password,u.hashed_password): raise HTTPException(401,"Incorrect credentials")
 return TokenResponse(access_token=token_for(u.id))
@router.get("/me")
async def me(u=Depends(current_user)): return {"id":u.id,"email":u.email,"role":u.role}
