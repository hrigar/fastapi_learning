# print('hekko hrishi') 

from multiprocessing import synchronize
from fastapi import Body, FastAPI, status, HTTPException, Depends, Response

from pydantic import BaseModel
import json
from typing import List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models
from .schemas import Post, PostResponse
app = FastAPI()


models.Base.metadata.create_all(bind=engine)




@app.get("/")
async def root():
    return {"name":"madman","lang":"fastapi",'happy':"no"}


@app.get("/posts",response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # posts = cur.execute("SELECT * FROM posts")
    # results = cur.fetchall()
    posts = db.query(models.Post).all()
    # print(posts)
    return  posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cur.execute("""INSERT INTO posts (title, content) values (%s,%s) returning *""",(post.title, post.content))
    # result = cur.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""select * from posts where id = %s """, (id,))
    # result = cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post found with id {id}")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""delete from posts where id = %s returning *""", (id,))
    # deleted_post = cur.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exisr")
    # conn.commit()
    post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=PostResponse)
def update_post(post_toupdate: Post, id: int, db: Session = Depends(get_db)):
    # cur.execute("""update posts set title = %s, content = %s where id = %s returning *""", (post.title, post.content, id))
    # updated_post = cur.fetchone()
    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
   
    post_query.update(post_toupdate.dict(), synchronize_session= False)
    db.commit()
    db.refresh(post)
    return post
    

# @app.get("/sqlalchemy")
# def alchemy(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

# try:
#     conn = psycopg2.connect(
#     dbname='fastapi',
#     user='postgres',
#     password='****',
#     host='localhost',  
#     port='5432',  
#     cursor_factory=RealDictCursor
#     )
#     cur = conn.cursor()
#     print('connection esstablished')

# except Exception as error:
#     print('connection failed')
#     print("error: ", error)


# # Closing the connection
# cur.close()
# conn.close()
# print("con closed")