# print('hekko hrishi') 

from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel
import json
from typing import List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title : str
    content :str

@app.get("/")
async def root():
    return {"name":"madman","lang":"fastapi",'happy':"no"}


@app.get("/posts")
def get_posts():
    posts = cur.execute("SELECT * FROM posts")
    results = cur.fetchall()
   
    return results

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute("""INSERT INTO posts (title, content) values (%s,%s) returning *""",(post.title, post.content))
    result = cur.fetchone()
    conn.commit()
    return result

@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""select * from posts where id = %s """, (id,))
    result = cur.fetchone()
    conn.commit()

    return result

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""delete from posts where id = %s returning *""", (id,))
    deleted_post = cur.fetchone()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()
    return deleted_post

@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    cur.execute("""update posts set title = %s, content = %s where id = %s returning *""", (post.title, post.content, id))
    updated_post = cur.fetchone()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    conn.commit()
    return updated_post
    

try:
    conn = psycopg2.connect(
    dbname='fastapi',
    user='postgres',
    password='****',
    host='localhost',  
    port='5432',  
    cursor_factory=RealDictCursor
    )
    cur = conn.cursor()
    print('connection esstablished')

except Exception as error:
    print('connection failed')
    print("error: ", error)


# # Closing the connection
cur.close()
conn.close()
print("con closed")