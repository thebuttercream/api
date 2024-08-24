from fastapi import FastAPI
from app.api.endpoints import pdi, employee

app = FastAPI()

app.include_router(pdi.router, prefix="/pdi", tags=["pdi"])
app.include_router(employee.router, prefix="/employees", tags=["employee"])
