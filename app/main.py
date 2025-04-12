from routers import auth, gift_card
from db import engine
from fastapi import FastAPI
from models.database import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(gift_card.router)

Base.metadata.create_all(bind=engine)

@app.get("/hello-world")
async def hello_world():
    return "Hello, world!"