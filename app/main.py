from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

def find_index_post(id):
    """This Function will take an ID as an Input and will delete the post"""
    for i,v in enumerate(my_posts):
        if v["id"] == id:
            return i


# @app -> This is the decorator and need to provide the instance name of FastAPI class, app, in this case
# get -> Method name
# "/" -> path
# root -> Function, can use any name
# Below funciton is for root of application

@app.get("/")
def root():
    return {"message": "First fastAPI running"}


# Write another function to retrieve the posts

@app.get("/posts")
def get_posts():
    return {"message": my_posts}

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {2} was not found"}
    return {"post detail": post}

    
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     """This func will take Body from input message, convert this to dictionay and save to payLoad variable"""
#     print(payLoad)
#     return{"new message is": f"title: {payLoad['title']} and content is: {payLoad['content']}"}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post : Post):
    """ This function will take the input data and will check the schema as per Post Class"""
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
    
    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # update = modify_post(id, post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"updated post": post_dict}



#############################################################
# execute main
#############################################################

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')