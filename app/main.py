from fastapi import FastAPI
from app.api.endpoints import person

app = FastAPI()

app.include_router(person.router, prefix="/person", tags=["person"])
