from fastapi import FastAPI
from app.api.endpoints import pdi, employee

app = FastAPI()

app.include_router(pdi.router, prefix="/pdicollection", tags=["pdi"])
app.include_router(employee.router, prefix="/employees", tags=["employee"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}
