from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel # this is the library to define the schema

import uvicorn

app = FastAPI()

class Post(BaseModel):
    """This Class will extend BaseModel Class and ensure that title is str and content is str"""
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"first title", "content": "first content", "id": 1}, {"title": "second title", "content": "second content", "id": 2}]

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
    
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     """This func will take Body from input message, convert this to dictionay and save to payLoad variable"""
#     print(payLoad)
#     return{"new message is": f"title: {payLoad['title']} and content is: {payLoad['content']}"}

@app.post("/posts")
def create_posts(post : Post):
    """ This function will take the input data and will check the schema as per Post Class"""
    print(post) # print the pydantic model
    print(post.dict()) # print the dictionary of pydantic model i.e. change the new_post
    return {"data": post}
    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')