from pathlib import Path
from app.services.storage import save
from app.config import get_settings
ALLOWED={".pdf",".png",".jpg",".jpeg",".txt"}
def ingest(owner,filename,data):
 if Path(filename).suffix.lower() not in ALLOWED: raise ValueError("Unsupported file type")
 if len(data)>get_settings().max_upload_mb*1024*1024: raise ValueError("File too large")
 p,h=save(owner,filename,data); return p,h
