from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional


class CareerBase(BaseModel):
    id: UUID
    name: str
    description: str
    softSkills: List[str]
    hardSkills: List[str]
    careerTrack: str
    behaviors: List[str]
    attitudes: List[str]
    seniority: str


class CareerRequest(BaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    softSkills: Optional[List[str]] = []
    hardSkills: Optional[List[str]] = []
    careerTrack: Optional[str] = ""
    behaviors: Optional[List[str]] = []
    attitudes: Optional[List[str]] = []
    seniority: Optional[str] = ""


class CareerResponse(BaseModel):
    id: str
    name: str
    description: str
    softSkills: List[str]
    hardSkills: List[str]
    careerTrack: str
    behaviors: List[str]
    attitudes: List[str]
    seniority: str


class CareerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    softSkills: Optional[List[str]] = None
    hardSkills: Optional[List[str]] = None
    careerTrack: Optional[str] = None
    behaviors: Optional[List[str]] = None
    attitudes: Optional[List[str]] = None
    seniority: Optional[str] = None
