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

from models.models import releases, comments, news, likes
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, ForeignKey, create_engine, select, insert, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_name = Column(String)

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
def account(request: Request):
    return templates.TemplateResponse("account-page.html", {"request": request})

@app.get("/catalog")
def catalog(request: Request):
    return templates.TemplateResponse("catalog-page.html", {"request": request})

@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("home-page.html", {"request": request})

@app.get("/cart")
def cart(request: Request):
    return templates.TemplateResponse("shopping-cart-page.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about-us-page.html", {"request": request})

@app.get("/item")
def item(request: Request):
    return templates.TemplateResponse("item-page.html", {"request": request})

@app.get("/reviews")
def item(request: Request):
    return templates.TemplateResponse("about-us-page.html", {"request": request})


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = engine = create_engine(DATABASE_URL)

session = Session(bind=engine)

@app.get("/get_news")
def get_products():
    try:
        query = select(news)
        data = session.execute(query)
        j = 0
        result = {"news" : []}
        for i in data.all():
            result['news'].append({})
            result['news'][j]["id"] = i[0]
            result['news'][j]["title"] = i[1]
            result['news'][j]["image_path"] = i[2]
            result['news'][j]["content"] = i[3]
            result['news'][j]["data"] = i[4]
            j+=1
        print(result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/get_releases")
def get_products():
    try:
        query = select(releases)
        data = session.execute(query)
        j = 0
        result = {"releases" : []}
        for i in data.all():
            result['releases'].append({})
            result['releases'][j]["release_id"] = i[0]
            result['releases'][j]["artist"] = i[1]
            result['releases'][j]["title"] = i[2]
            result['releases'][j]["image_path"] = i[3]
            result['releases'][j]["content"] = i[4]
            result['releases'][j]["link"] = i[5]
            
            j+=1
        print(result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/get_release/{release_id}")
async def get_release(release_id: int):
    try:
        query = select(releases).where(releases.c.release_id == f"{release_id}")
        result = session.execute(query)
        arr = result.all()[0]
        query = select(comments).where(comments.c.release_id == f"{release_id}")
        result = session.execute(query)
        arr2 = result.all()[0]
        S = {"release_id": arr[0], "artist": arr[1], "title" : arr[2], "image_path" : arr[3], "content" : arr[4], "link" : arr[5], "comments" : arr2}
        return S
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    


@app.post("/post_comment/{id}/{release_id}/{content}")
async def post_comment(id: int, release_id: int, content: str):
    try:
        stmt = insert(comments).values(id=f"{id}", release_id=f"{release_id}", content=f"{content}")
        result = session.execute(stmt)
        session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
@app.post("/post_release/{artist}/{title}/{content}")
async def post_release(artist: str, title: str, content: str):
    try:
        stmt = insert(comments).values(id=f"{id}", title=f"{title}", content=f"{content}")
        result = session.execute(stmt)
        session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.post("/post_like/{id}/{release_id}")
async def post_like(id: int, release_id: int):
    try:
        stmt = insert(likes).values(id=f"{id}", release_id=f"{release_id}")
        result = session.execute(stmt)
        session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/delete_like/{id}/{release_id}")
async def delete_like(id: int, release_id: int):
    try:
        record_to_delete = (
            session.query(Cart)
            .filter_by(id=id, release_id=release_id)
            .first()
        )
        if record_to_delete:
            session.delete(record_to_delete)

        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

    
@app.get("/cart_items/{user_id}")
async def cart_items(user_id: str):
    query = (
        select(
            rifle.c.name,
            rifle.c.price,
        )
        .select_from(carts.join(rifle, carts.c.product_name == rifle.c.name))
        .where(carts.c.user_id == user_id)
    )
    result = session.execute(query)

    rows = result.all()

    return {"products": [i[0] for i in rows], "total_sum" : sum([int(i[1]) for i in rows])}
    
    
@app.post("/delete_cart/{user_id}")
async def delete_cart(user_id: str):
    try:
        records_to_delete = (
            session.query(Cart)
            .filter_by(user_id=user_id)
            .all()
        )
        
        for record in records_to_delete:
            session.delete(record)

        session.commit()
        
        return {"detail": "Cart items deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")