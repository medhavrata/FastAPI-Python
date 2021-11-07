from fastapi import FastAPI
from fastapi.params import Body
import uvicorn

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
    
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    """This func will take Body from input message, convert this to dictionay and save to payLoad variable"""
    print(payLoad)
    return{"new message is": f"title: {payLoad['title']} and content is: {payLoad['content']}"}
    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')