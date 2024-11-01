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