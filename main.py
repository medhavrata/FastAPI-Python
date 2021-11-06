from fastapi import FastAPI

app = FastAPI()

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
    return{"message": "Here are your posts, enjoy your day"}