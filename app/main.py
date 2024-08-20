from fastapi import FastAPI
from app.api.endpoints import auth, pdi, employee

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(pdi.router, prefix="/pdicollection", tags=["pdi"])
app.include_router(employee.router, prefix="/employees", tags=["employee"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}
