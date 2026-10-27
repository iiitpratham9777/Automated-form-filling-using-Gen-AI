from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine,Base
from app.api.auth import router as auth
from app.api.documents import router as documents
from app.api.profile import router as profile
from app.api.automation import router as automation
@asynccontextmanager
async def lifespan(app):
 async with engine.begin() as c: await c.run_sync(Base.metadata.create_all)
 yield; await engine.dispose()
app=FastAPI(title="FormPilot AI",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://localhost:3000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth,prefix="/api");app.include_router(documents,prefix="/api");app.include_router(profile,prefix="/api");app.include_router(automation,prefix="/api")
@app.get("/health")
async def health(): return {"status":"ok","service":"formpilot-backend"}
