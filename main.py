from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import Field

from fastapi import FastAPI, Depends, HTTPException
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

from models.models import rifle, carts
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, ForeignKey, create_engine, select, insert
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
    try:
        query = select(rifle)
        data = session.execute(query)
        j = 0
        result = {"products" : []}
        for i in data.all():
            result['products'].append({})
            result['products'][j]["name"] = i[1]
            result['products'][j]["brand"] = i[2]
            result['products'][j]["price"] = i[3]
            result['products'][j]["calibr"] = i[4]
            result['products'][j]["image_path"] = i[5]
            j+=1
        print(result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/add_to_cart/{user_id}/{product_name}")
async def add_to_cart(user_id: int, product_name: str):
    try:
        stmt = insert(carts).values(user_id=f"{user_id}", product_name=f"{product_name}")
        result = session.execute(stmt)
        session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/cart_items/{user_id}")
async def add_to_cart(user_id: int):
    query = select(carts).where(carts.c.user_id == f"{user_id}")
    result = session.execute(query)
    S = {"products": [i[2] for i in result.all()]}
    print(S)
    return S

    
@app.get("/product/{product_name}")
async def add_to_cart(product_name: int):
    try:
        query = select(rifle).where(rifle.c.name == f"{product_name}")
        result = session.execute(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")