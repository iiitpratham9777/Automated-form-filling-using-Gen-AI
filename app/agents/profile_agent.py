PRIORITY={"aadhaar":.98,"pan":.98,"degree":.92,"marksheet":.9,"resume":.75,"unknown":.3}
ALIASES={"full_name":{"candidate_name","name"},"pan":{"pan"},"email":{"email"},"phone":{"phone"},"dob":{"dob"},"cgpa":{"cgpa"}}
def build(docs):
 c={}
 for d in docs:
  for e in d["entities"]:
   f=next((k for k,v in ALIASES.items() if e["name"] in v),e["name"]); c.setdefault(f,[]).append({"value":e["normalized_value"],"source":d["filename"],"document_type":d["document_type"],"confidence":e["confidence"],"source_reliability":PRIORITY.get(d["document_type"],.3)})
 profile={}; conflicts=[]
 for f,vals in c.items():
  vals.sort(key=lambda x:(x["source_reliability"],x["confidence"]),reverse=True); profile[f]=vals[0]
  if len({x["value"] for x in vals})>1: conflicts.append({"field":f,"values":vals})
 return profile,conflicts
