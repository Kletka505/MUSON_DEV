from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import Field

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from server.auth import auth_backend
from server.database import User
from server.manager import get_user_manager
from fastapi.middleware.cors import CORSMiddleware
from server.schemas import UserRead, UserCreate, UserUpdate

from models.models import rifle
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, ForeignKey, create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session



app = FastAPI(
    title="StrikeEmAll",
    static_folder='./src/static',
    template_folder='./src/templates'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="pages")


@app.get("/account")
def unprotected_route(request: Request):
    return templates.TemplateResponse("account-page.html", {"request": request})

@app.get("/catalog")
def unprotected_route(request: Request):
    return templates.TemplateResponse("catalog-page.html", {"request": request})

@app.get("/home")
def unprotected_route(request: Request):
    return templates.TemplateResponse("home-page.html", {"request": request})

@app.get("/cart")
def unprotected_route(request: Request):
    return templates.TemplateResponse("shopping-cart-page.html", {"request": request})

@app.get("/about")
def unprotected_route(request: Request):
    return templates.TemplateResponse("about-us-page.html", {"request": request})

@app.get("/item")
def unprotected_route(request: Request):
    return templates.TemplateResponse("item-page.html", {"request": request})



DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = engine = create_engine(DATABASE_URL)

session = Session(bind=engine)

@app.get("/rifle")
def get_rifles():
    query = select(rifle)
    result = session.execute(query)
    j = 0
    S = {"products" : []}
    for i in result.all():
        S['products'].append({})
        S['products'][j]["name"] = i[1]
        S['products'][j]["brand"] = i[2]
        S['products'][j]["price"] = i[3]
        S['products'][j]["calibr"] = i[4]
        S['products'][j]["image_path"] = i[5]
        j+=1
    
    return S

@app.get("/product")
def get_rifles():
    return

