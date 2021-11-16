from app.database import Base
from pydantic import BaseModel, EmailStr # this is the library to define the schema
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# THIS IS THE SCHEMA FOR INPUT AND OUTPUT 
# USER WILL ONLY BE ABLE TO SEND THE INPUT REQUEST
# AS PER THE INPUT SCHEMA DEFINED AND THE APPLICATION
# WILL SEND BACK THE RESPONSE AS PER THE RESPONSE
# SCHEMA DEFINED

# BELOW IS THE SCHEMA FOR THE USER CREATION
class UserCreate(BaseModel):
    """This Class will extend BaseModel to define the Schema for User Creation"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

# BELOW IS THE SCHEMA FOR THE USER AUTHENTICATION

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# BELOW IS THE SCHEMA FOR POST 

class PostBase(BaseModel):
    """This Class will extend BaseModel Class and ensure that title is str and content is str"""
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    """This Class is to define the schema to create a Post"""
    pass

class PostUpdate(PostBase):
    """This Class is to define the schema to update a post"""
    pass

class PostResponse(PostBase):
    """This Class is to define the Schema for API Response"""
    id : int
    created_at : datetime
    owner_id : int
    owner: UserResponse # This is working as we have defined a relationship in the models between Post and User for 'owner' field

    #Need to include below class to tell pydantic model that we are working with orm mode so work without expecting dictionary
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True



# BELOW IS THE SCHEMA FOR TOKEN

class Token(BaseModel):
    access_token: str
    token_type: str

# BELOW IS THE SCHEMA FOR TOKEN DATA

class TokenData(BaseModel):
    id: Optional[str] = None


# BELOW IS THE SCHEMA FOR VOTE

class VoteCreate(BaseModel):
    post_id: int
    post_direction: conint(le=1)
