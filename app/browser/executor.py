from playwright.async_api import async_playwright
async def execute(url,mappings):
 async with async_playwright() as pw:
  b=await pw.chromium.launch(headless=True); p=await b.new_page(); await p.goto(url,wait_until="domcontentloaded"); actions=[]
  for m in mappings:
   loc=p.locator(f'[name="{m["field"]}"],#{m["field"]}').first
   if await loc.count()==0: actions.append({"field":m["field"],"ok":False,"error":"field_not_found"}); continue
   await loc.fill(str(m["value"])); actual=await loc.input_value(); actions.append({"field":m["field"],"ok":actual==str(m["value"]),"actual":actual})
  await b.close(); return {"actions":actions}
