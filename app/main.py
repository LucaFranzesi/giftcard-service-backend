from configurations import config
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello-world")
async def hello_world():
    return "Hello, world!"