from fastapi import FastAPI
from app.api.endpoints import person, career

app = FastAPI()

app.include_router(career.router, prefix="/career", tags=["career"])
app.include_router(person.router, prefix="/person", tags=["person"])
