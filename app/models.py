import uuid
from datetime import datetime,timezone
from sqlalchemy import String,Text,Float,Boolean,ForeignKey,DateTime,JSON,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.db import Base
def uid(): return str(uuid.uuid4())
def now(): return datetime.now(timezone.utc)
class User(Base):
 __tablename__="users"; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); email:Mapped[str]=mapped_column(String(320),unique=True,index=True); hashed_password:Mapped[str]=mapped_column(Text); role:Mapped[str]=mapped_column(String(32),default="user"); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Document(Base):
 __tablename__="documents"; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); user_id:Mapped[str]=mapped_column(ForeignKey("users.id")); filename:Mapped[str]=mapped_column(Text); mime_type:Mapped[str]=mapped_column(String(128)); sha256:Mapped[str]=mapped_column(String(64),index=True); storage_path:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); __table_args__=(UniqueConstraint("user_id","sha256"),)
class DocumentEntity(Base):
 __tablename__="document_entities"; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); document_id:Mapped[str]=mapped_column(ForeignKey("documents.id")); name:Mapped[str]=mapped_column(String(128),index=True); raw_value:Mapped[str]=mapped_column(Text); normalized_value:Mapped[str]=mapped_column(Text); confidence:Mapped[float]=mapped_column(Float); method:Mapped[str]=mapped_column(String(32))
class Profile(Base):
 __tablename__="profiles"; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); user_id:Mapped[str]=mapped_column(ForeignKey("users.id"),unique=True); data:Mapped[dict]=mapped_column(JSON,default=dict); conflicts:Mapped[list]=mapped_column(JSON,default=list); verified:Mapped[bool]=mapped_column(Boolean,default=False); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
class AutomationRun(Base):
 __tablename__="automation_runs"; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); user_id:Mapped[str]=mapped_column(ForeignKey("users.id")); target_url:Mapped[str]=mapped_column(Text); status:Mapped[str]=mapped_column(String(32),default="created"); state:Mapped[dict]=mapped_column(JSON,default=dict); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class AuditLog(Base):
 __tablename__="audit_logs"; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); run_id:Mapped[str]=mapped_column(String(36),index=True); agent:Mapped[str]=mapped_column(String(64)); action:Mapped[str]=mapped_column(String(64)); payload:Mapped[dict]=mapped_column(JSON,default=dict); status:Mapped[str]=mapped_column(String(32),default="ok"); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
