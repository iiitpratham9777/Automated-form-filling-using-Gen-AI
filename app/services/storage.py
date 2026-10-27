from pathlib import Path
import hashlib
from app.config import get_settings
root=Path(get_settings().storage_dir); root.mkdir(parents=True,exist_ok=True)
def save(owner,filename,data):
 digest=hashlib.sha256(data).hexdigest(); d=root/owner; d.mkdir(parents=True,exist_ok=True); p=d/(digest[:16]+"_"+Path(filename).name); p.write_bytes(data); return str(p),digest
