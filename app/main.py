from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import input_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(input_user.router)


