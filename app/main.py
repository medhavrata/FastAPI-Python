from fastapi import FastAPI
import uvicorn
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# This is the command which tells alchemy to create the table, but if using alembic, no need to use this. CAN BE COMMENTED OUT.
# models.Base.metadata.create_all(bind=engine) 


app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#my_posts = [{"title":"first title", "content": "first content", "id": 1}, {"title": "second title", "content": "second content", "id": 2}]

# def find_post(id):
#     """This function will take an ID as an Input and return back the post"""
#     for post in my_posts:
#         if post["id"] == id:
#             return post

# def find_index_post(id):
#     """This Function will take an ID as an Input and will delete the post"""
#     for i,v in enumerate(my_posts):
#         if v["id"] == id:
#             return i


# We have moved the post and user functionaltiy to separate files, so now when the HTTP request comes, it will check the router
# and go into post and user files to check for a route.

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# @app -> This is the decorator and need to provide the instance name of FastAPI class, app, in this case
# get -> Method name
# "/" -> path
# root -> Function, can use any name
# Below funciton is for root of application

@app.get("/")
def root():
    return {"message": "First fastAPI running"}

###################################################################################
# TEST FUNCTION
###################################################################################

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"Result": posts}

###################################################################################


# Write another function to retrieve the posts


#############################################################
# execute main
#############################################################

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')