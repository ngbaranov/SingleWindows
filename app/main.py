from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import input_user, index, get_user_id, input_violation, get_search, advanced_search

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(index.router)
app.include_router(input_user.router)
app.include_router(get_user_id.router)
app.include_router(input_violation.router)
app.include_router(get_search.router)
app.include_router(advanced_search.router)





