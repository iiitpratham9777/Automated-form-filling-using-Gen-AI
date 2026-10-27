from playwright.async_api import async_playwright
async def inspect(url):
 async with async_playwright() as pw:
  b=await pw.chromium.launch(headless=True); p=await b.new_page(); await p.goto(url,wait_until="domcontentloaded")
  fs=await p.locator("input,select,textarea").evaluate_all("""els=>els.map(e=>({name:e.name||e.id||'',id:e.id||'',type:e.type||e.tagName.toLowerCase(),required:!!e.required,label:e.labels&&e.labels.length?e.labels[0].innerText:'',options:e.tagName.toLowerCase()==='select'?Array.from(e.options).map(o=>({text:o.textContent.trim(),value:o.value})):[]}))""")
  title=await p.title(); await b.close(); return {"url":url,"title":title,"fields":fs}
