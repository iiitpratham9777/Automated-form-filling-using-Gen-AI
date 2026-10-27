from pathlib import Path
import re,fitz
from PIL import Image
import pytesseract
P={"pan":re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"),"phone":re.compile(r"\b[6-9][0-9]{9}\b"),"email":re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),"cgpa":re.compile(r"(?i)\b(?:cgpa|c\.g\.p\.a)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"),"dob":re.compile(r"(?i)\b(?:dob|date of birth)\s*[:=-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")}
def text(path):
 p=Path(path)
 if p.suffix.lower()==".pdf":
  doc=fitz.open(path); t="\n".join(x.get_text() for x in doc).strip()
  if t:return t,.98
  imgs=[]
  for page in doc:
   px=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)); imgs.append(Image.frombytes("RGB",[px.width,px.height],px.samples))
  return "\n".join(pytesseract.image_to_string(i) for i in imgs),.80
 if p.suffix.lower() in {".png",".jpg",".jpeg"}: return pytesseract.image_to_string(Image.open(path)),.80
 return p.read_text(errors="ignore"),.95
def classify(fn,t):
 s=(fn+" "+t[:3000]).lower(); rules=[("pan",["pan","income tax"]),("aadhaar",["aadhaar","uidai"]),("resume",["resume","curriculum vitae"]),("degree",["degree","b.tech","bachelor","cgpa"]),("marksheet",["marksheet","secondary","senior secondary"])]
 best="unknown"; conf=.3
 for lab,keys in rules:
  hits=sum(k in s for k in keys)
  if hits and .55+.12*hits>conf: best,conf=lab,min(.95,.55+.12*hits)
 return best,conf
def entities(t):
 out=[]
 for n,p in P.items():
  for m in p.finditer(t): out.append({"name":n,"raw_value":m.group(1) if m.lastindex else m.group(0),"confidence":.93,"method":"regex"})
 return out
def norm(n,v): return v.strip().upper() if n=="pan" else v.strip()
