from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


# ==========================================
# USER SCHEMAS
# ==========================================
class UserCreate(BaseModel):  # Capitalized 'C' for standard naming conventions
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    # Modern Pydantic v2 configuration replaces 'class Config'
    model_config = ConfigDict(from_attributes=True)



class TaskCreate(BaseModel):  
    title: str
    description: Optional[str] = None  
    completed: bool = (
        False 
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

   
    model_config = ConfigDict(from_attributes=True)
