from fastapi import APIRouter,Depends,File,UploadFile,HTTPException
from sqlalchemy import select
from app.db import get_db
from app.models import Document,DocumentEntity
from app.security import current_user
from app.agents.intake import ingest
from app.agents.document_agent import process
router=APIRouter(prefix="/documents")
@router.post("/upload")
async def upload(files:list[UploadFile]=File(...),u=Depends(current_user),db=Depends(get_db)):
 out=[]
 for f in files:
  data=await f.read()
  try:p,h=ingest(u.id,f.filename or "file",data)
  except ValueError as e: raise HTTPException(400,str(e))
  if (await db.execute(select(Document).where(Document.user_id==u.id,Document.sha256==h))).scalar_one_or_none(): continue
  d=Document(user_id=u.id,filename=f.filename or "file",mime_type=f.content_type or "application/octet-stream",sha256=h,storage_path=p); db.add(d); await db.flush(); r=process(p,d.filename)
  for e in r["entities"]: db.add(DocumentEntity(document_id=d.id,name=e["name"],raw_value=e["raw_value"],normalized_value=e["normalized_value"],confidence=e["confidence"],method=e["method"]))
  out.append({"id":d.id,"filename":d.filename,"classification":r["document_type"],"entities":r["entities"]})
 await db.commit(); return {"documents":out}
