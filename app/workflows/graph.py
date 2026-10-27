from langgraph.graph import StateGraph,START,END
from app.workflows.state import State
from app.agents.document_agent import process
from app.agents.profile_agent import build
from app.browser.inspector import inspect
from app.agents.mapper import map_fields
async def pipeline(s):
 docs=[process(d["path"],d["filename"]) for d in s.get("documents",[])]; profile,conf=build(docs); return {"processed_documents":docs,"profile":profile,"conflicts":conf}
async def inspect_map(s):
 schema=await inspect(s["target_url"]); return {"form_schema":schema,"mappings":map_fields(schema["fields"],s.get("profile",{}))}
def checkpoint(s): return {"checkpoint":{"required":True,"reason":"Review mappings before browser execution"}}
def build_graph():
 g=StateGraph(State); g.add_node("pipeline",pipeline); g.add_node("inspect_map",inspect_map); g.add_node("checkpoint",checkpoint); g.add_edge(START,"pipeline"); g.add_edge("pipeline","inspect_map"); g.add_edge("inspect_map","checkpoint"); g.add_edge("checkpoint",END); return g.compile()
