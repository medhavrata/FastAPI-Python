from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel # this is the library to define the schema
from random import randrange

import uvicorn

app = FastAPI()

class Post(BaseModel):
    """This Class will extend BaseModel Class and ensure that title is str and content is str"""
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"first title", "content": "first content", "id": 1}, {"title": "second title", "content": "second content", "id": 2}]

def find_post(id):
    """This function will take an ID as an Input and return back the post"""
    for post in my_posts:
        if post["id"] == id:
            return post

# @app -> This is the decorator and need to provide the instance name of FastAPI class, app, in this case
# get -> Method name
# "/" -> path
# root -> Function, can use any name
# Below funciton is for root of application

@app.get("/")
async def root():
    return {"message": "First fastAPI running"}


# Write another function to retrieve the posts

@app.get("/posts")
def get_posts():
    return {"message": my_posts}

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    return {"post detail": post}

    
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     """This func will take Body from input message, convert this to dictionay and save to payLoad variable"""
#     print(payLoad)
#     return{"new message is": f"title: {payLoad['title']} and content is: {payLoad['content']}"}

@app.post("/posts")
def create_posts(post : Post):
    """ This function will take the input data and will check the schema as per Post Class"""
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')