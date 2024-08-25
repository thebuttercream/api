from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class SkillBase(BaseModel):
    id: UUID
    name: str
    type: str
    category: str


class SkillRequest(BaseModel):
    name: Optional[str] = ""
    type: Optional[str] = ""
    category: Optional[str] = ""


class SkillResponse(BaseModel):
    id: str
    name: str
    type: str
    category: str


class SkillUpdate(BaseModel):
    name: Optional[str] = ""
    type: Optional[str] = ""
    category: Optional[str] = ""
