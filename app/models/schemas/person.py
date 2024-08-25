from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class PersonBase(BaseModel):
    id: UUID
    name: str
    formation: str
    maritalStatus: str
    location: str
    age: int
    position: str
    livingWith: str
    lifeGoal: str

class PersonRequest(BaseModel):
    name: Optional[str] = ""
    formation: Optional[str] = ""
    maritalStatus: Optional[str] = ""
    location: Optional[str] = ""
    age: Optional[int] = 0
    position: Optional[str] = ""
    livingWith: Optional[str] = ""
    lifeGoal: Optional[str] = ""

class PersonResponse(BaseModel):
    id: str
    name: str
    formation: str
    maritalStatus: str
    location: str
    age: int
    position: str
    livingWith: str
    lifeGoal: str

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    formation: Optional[str] = None
    maritalStatus: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    position: Optional[str] = None
    livingWith: Optional[str] = None
    lifeGoal: Optional[str] = None
