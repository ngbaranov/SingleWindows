from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import (input_user, index, get_user_id, input_violation, get_search, advanced_search, keyword_search,
                         add_document, delete_user, admin_panel)
from auth import auth_routher

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(index.router)
app.include_router(input_user.router)
app.include_router(get_user_id.router)
app.include_router(input_violation.router)
app.include_router(get_search.router)
app.include_router(advanced_search.router)
app.include_router(keyword_search.router)
app.include_router(add_document.router)
app.include_router(delete_user.router)
app.include_router(auth_routher.router)
app.include_router(admin_panel.router)





