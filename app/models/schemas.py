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
