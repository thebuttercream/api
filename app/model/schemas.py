from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    password: Optional[str] = None


class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class CPFIdentify(BaseModel):
    cpf: str


class Token(BaseModel):
    access_token: str
    employee_id: int


class TokenData(BaseModel):
    username: Optional[str] = None
