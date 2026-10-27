from typing import TypedDict,Any
class State(TypedDict,total=False):
 run_id:str; user_id:str; target_url:str; documents:list[dict]; processed_documents:list[dict]; profile:dict; conflicts:list[dict]; form_schema:dict; mappings:list[dict]; checkpoint:dict; execution:dict
