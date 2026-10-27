from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from app.db import get_db
from app.models import AutomationRun,Profile,AuditLog
from app.security import current_user
from app.schemas.models import AutomationStart,CheckpointResume
from app.workflows.graph import build_graph
from app.browser.executor import execute
router=APIRouter(prefix="/automation")
@router.post("/start")
async def start(b:AutomationStart,u=Depends(current_user),db=Depends(get_db)):
 p=(await db.execute(select(Profile).where(Profile.user_id==u.id))).scalar_one_or_none()
 if not p: raise HTTPException(400,"Build a profile first")
 run=AutomationRun(user_id=u.id,target_url=b.target_url,status="planning");db.add(run);await db.commit();await db.refresh(run)
 # The graph receives the profile directly; document reprocessing is optional at this stage.
 g=build_graph(); state=await g.ainvoke({"run_id":run.id,"user_id":u.id,"target_url":b.target_url,"documents":[],"profile":p.data})
 run.state=state;run.status="awaiting_approval";db.add(AuditLog(run_id=run.id,agent="checkpoint",action="awaiting_approval",payload={"mappings":state.get("mappings",[])}));await db.commit();return {"id":run.id,"status":run.status,"state":state}
@router.get("/{run_id}")
async def get_run(run_id,u=Depends(current_user),db=Depends(get_db)):
 r=(await db.execute(select(AutomationRun).where(AutomationRun.id==run_id,AutomationRun.user_id==u.id))).scalar_one_or_none()
 if not r: raise HTTPException(404,"Run not found")
 return {"id":r.id,"status":r.status,"state":r.state}
@router.post("/{run_id}/resume")
async def resume(run_id,b:CheckpointResume,u=Depends(current_user),db=Depends(get_db)):
 r=(await db.execute(select(AutomationRun).where(AutomationRun.id==run_id,AutomationRun.user_id==u.id))).scalar_one_or_none()
 if not r: raise HTTPException(404,"Run not found")
 if r.status!="awaiting_approval": raise HTTPException(400,"Run is not awaiting approval")
 if b.action=="reject": r.status="cancelled"
 elif b.action=="edit": r.state={**r.state,"profile":{**r.state.get("profile",{}),**b.edits}}
 else:
  result=await execute(r.target_url,r.state.get("mappings",[]));r.state={**r.state,"execution":result,"checkpoint":{"required":False}};r.status="completed" if all(x["ok"] for x in result["actions"]) else "failed";db.add(AuditLog(run_id=r.id,agent="browser_executor",action="execute",payload=result,status=r.status))
 await db.commit();return {"id":r.id,"status":r.status,"state":r.state}
