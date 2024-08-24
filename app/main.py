from fastapi import FastAPI
from app.api.endpoints import pdi, employee, person

app = FastAPI()

app.include_router(pdi.router, prefix="/pdi", tags=["pdi"])
app.include_router(employee.router, prefix="/employee", tags=["employee"])
app.include_router(person.router, prefix="/person", tags=["person"])
