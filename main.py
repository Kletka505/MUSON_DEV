from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import Field

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
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
import shutil, os

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
        delete_stmt = (
            delete(likes)
            .where(likes.c.id == id)
            .where(likes.c.release_id == release_id)
        )
        result = session.execute(delete_stmt)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/get_like/{id}/{release_id}")
def get_products(id: int, release_id: int):
    try:
        query = select(likes).where(likes.c.id == id).where(likes.c.release_id == release_id)
        data = session.execute(query)
        j = 0
        result = {"likes" : []}
        for i in data.all():
            result['likes'].append({})
            result['likes'][j]["like_id"] = i[0]
            result['likes'][j]["id"] = i[1]
            result['likes'][j]["release_id"] = i[2]
            j+=1
        if result['likes']:
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.post("/upload_release/")
async def upload_release(artist: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    link: str = Form(...),
    image: UploadFile = File(...),
    archive: UploadFile = File(...)
):
    try:
        with open(f"uploads/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        with open(f"uploads/{archive.filename}", "wb") as buffer:
            shutil.copyfileobj(archive.file, buffer)
        
        image_path = f"uploads/{image.filename}"
        archive_path = f"uploads/{archive.filename}"

        release_data = {
            "artist": artist,
            "title": title,
            "image_path": image_path,
            "archive_path": archive_path,
            "content": content,
            "link": link,
            "archive_path": archive_path,
        }
        insert_query = releases.insert().values(**release_data)
        session.execute(insert_query)
        session.commit()
        
        return {"message": "Release uploaded successfully", "image_path": image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.post("/upload_news/")
async def upload_release(title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(...),
    
):
    try:
        with open(f"uploads/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_path = f"uploads/{image.filename}"
        release_data = {
            "title": title,
            "image_path": image_path,
            "content": content,
            "date": date,
        }
        insert_query = news.insert().values(**release_data)
        session.execute(insert_query)
        session.commit()
        
        return {"message": "News uploaded successfully", "image_path": image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/download_archive/{release_id}")
async def download_archive(release_id: int):
    # Поиск записи по release_id
    query = select(releases).where(releases.c.release_id == release_id)
    result = session.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Release not found")

    archive_path = result.archive_path

    # Проверка существования файла
    if not os.path.isfile(archive_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Возврат файла
    return FileResponse(archive_path, filename=os.path.basename(archive_path), media_type='application/octet-stream')