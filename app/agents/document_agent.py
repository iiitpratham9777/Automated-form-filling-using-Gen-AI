from app.services.extraction import text,classify,entities,norm
def process(path,filename):
 t,ocr=text(path); typ,cc=classify(filename,t); es=entities(t)
 for e in es:e["normalized_value"]=norm(e["name"],e["raw_value"])
 return {"filename":filename,"path":path,"document_type":typ,"classification_confidence":cc,"ocr_quality":ocr,"entities":es}
