from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    prefix = "/users", # This will prefix each request with the specified value
    tags = ["Users"] # This will create a tag on the documentation
)



###################################################################################
# FUNCTION NAME: CREATE_USER
# THIS FUNCTION WILL CREATE A USER IN USERS TABLE IN FASTAPI DATABASE
# While testing from Postman, we have used the path "/users" and not "/users/" but while testing in this file
# we have used the path "/users/" and if we use just "/users", it is failing, but why?
# because, when we send a request to path "/users", it will be redirected to path "/users/" and the response
# code will be '307', which will not match with '201' and the test fails
###################################################################################
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_users(user : schemas.UserCreate, db: Session = Depends(get_db)):
    """ This function will take the input data and will check the schema as per Post Class"""
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Hash the User Password before storing into database

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

###################################################################################
# FUNCTION NAME: CREATE_USER
# THIS FUNCTION WILL CREATE A USER IN USERS TABLE IN FASTAPI DATABASE
###################################################################################
@router.get("/{id}", response_model = schemas.UserResponse)
def get_users(id : int, db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.id == id).first()
    if not find_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"post with id: {2} was not found"}
    return find_user
