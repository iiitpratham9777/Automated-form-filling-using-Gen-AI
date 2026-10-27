from pydantic import BaseModel,EmailStr,Field
class RegisterRequest(BaseModel): email:EmailStr; password:str=Field(min_length=8,max_length=128)
class TokenResponse(BaseModel): access_token:str; token_type:str="bearer"
class AutomationStart(BaseModel): target_url:str
class CheckpointResume(BaseModel): action:str=Field(pattern="^(approve|reject|edit)$"); edits:dict={}
