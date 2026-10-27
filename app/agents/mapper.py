ALIASES={"full_name":["full_name","name","legal_name"],"dob":["dob","birth"],"email":["email","mail"],"phone":["phone","mobile"],"pan":["pan"],"cgpa":["cgpa"]}
def map_fields(fields,profile):
 out=[]
 for f in fields:
  hay=(f.get("name","")+" "+f.get("id","")+" "+f.get("label","")).lower()
  for key,aliases in ALIASES.items():
   if key in profile and any(a in hay for a in aliases): out.append({"field":f["name"],"profile_key":key,"value":profile[key]["value"],"confidence":.92,"strategy":"rule"}); break
 return out
