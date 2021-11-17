from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# THE BELOW IS THE MODEL TO DEFINE THE TABLES IN DATABASE. NEED TO PROVIDE
# THE TABLE NAME AND THE COLUMNS AND EACH TIME WHEN THE PROGRAM
# WILL RUN, IT WILL CHECK WHETHER THE TABLE EXISTS ALREADY OR NOT
# IF NOT, A NEW TABLE WILL BE CREATED. BUT IF WE JUST UPDATE 
# THE COLUMN OF AN EXISTING TABLE, IT WILL NOT UPDATE THE 
# NEW COLUMN IN THE EXISTING TABLE. THIS IS A CONSTRAINT WITH SQLALCHEMY
# THAT IT DOES NOT UPDATE THE COLUMN IN AN EXISTING TABLE

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User") # This will return back the owner which will contain the values of User table for that particular id


# BELOW IS THE MODEL TO DEFINE THE USERS TABLE. THIS TABLE IS BEING
# CREATED TO ADD THE USERS FOR THE APPLICATIONS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(Integer, nullable=True)

# BELOW IS THE MODEL TO DEFINE THE VOTES TABLE. THIS TABLE IS BEING 
# CREATED TO STORE THE LIKES ON THE POST BY THE USER

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True )
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)