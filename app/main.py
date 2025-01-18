from routers import auth, gift_card
from db import engine
from fastapi import FastAPI
from models.database import Base

app = FastAPI()

app.include_router(auth.router)
app.include_router(gift_card.router)

Base.metadata.create_all(bind=engine)

@app.get("/hello-world")
async def hello_world():
    return "Hello, world!"