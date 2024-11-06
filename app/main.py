from fastapi import FastAPI

from app.routers import input_user

app = FastAPI()

app.include_router(input_user.router)


