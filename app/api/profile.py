from fastapi import APIRouter,Depends
from sqlalchemy import select
from app.db import get_db
from app.models import Profile,Document,DocumentEntity
from app.security import current_user
from app.agents.profile_agent import build
router=APIRouter(prefix="/profile")
@router.post("/build")
async def build_profile(u=Depends(current_user),db=Depends(get_db)):
 docs=(await db.execute(select(Document).where(Document.user_id==u.id))).scalars().all(); processed=[]
 for d in docs:
  es=(await db.execute(select(DocumentEntity).where(DocumentEntity.document_id==d.id))).scalars().all(); processed.append({"filename":d.filename,"document_type":"unknown","entities":[{"name":e.name,"normalized_value":e.normalized_value,"raw_value":e.raw_value,"confidence":e.confidence} for e in es]})
 data,conf=build(processed); p=(await db.execute(select(Profile).where(Profile.user_id==u.id))).scalar_one_or_none()
 if not p:p=Profile(user_id=u.id,data=data,conflicts=conf); db.add(p)
 else:p.data=data;p.conflicts=conf
 await db.commit(); return {"data":data,"conflicts":conf,"verified":p.verified}
