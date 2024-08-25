from fastapi import FastAPI
from app.api.endpoints import career, person, skill

app = FastAPI()

app.include_router(career.router, prefix="/career", tags=["career"])
app.include_router(person.router, prefix="/person", tags=["person"])
app.include_router(skill.router, prefix="/skill", tags=["skill"])
