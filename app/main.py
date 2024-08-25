from fastapi import FastAPI
from app.api.endpoints import pdi, person

app = FastAPI()

app.include_router(pdi.router, prefix="/pdi", tags=["pdi"])
app.include_router(person.router, prefix="/person", tags=["person"])
