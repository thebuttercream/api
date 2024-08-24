from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# PDI
class PDIBase(BaseModel):
    pdi: str

class PDIInDB(PDIBase):
    id: str
    date_add: datetime

class PDIResponse(PDIBase):
    id: str
    date_add: datetime

class PDIRequest(PDIBase):
    pdi: str

# Employee
class EmployeeBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    cpf: str

class EmployeeResponse(EmployeeBase):
    id: str

class EmployeeUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    password: Optional[str] = None


# Person
class PersonBase(BaseModel):
    name: str
    formation: str
    maritalStatus: str
    location: str
    age: int
    position: str
    livingWith: str
    lifeGoal: str


class PersonResponse(PersonBase):
    id: str


class PersonUpdate(BaseModel):
    name: Optional[str] = None
    formation: Optional[str] = None
    maritalStatus: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    position: Optional[str] = None
    livingWith: Optional[str] = None
    lifeGoal: Optional[str] = None
