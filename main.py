from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from blog.database import engine

from blog import models

app=FastAPI()


models.Base.metadata.create_all(engine)

class Blog(BaseModel):
    title:str
    published:Optional[bool]


@app.get("/")
def index():
    return {'data':{"name":"Aakash"}}


@app.get("/about/")
def about(limit: int):
    return {'data':f"Showing DATA {limit} from db"}

@app.get("/about/{id}")
def about(id : int):
    return{"data": id}


@app.post("/blog")
def create_blog(request : Blog):
    return {"Blog"}