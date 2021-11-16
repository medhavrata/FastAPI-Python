from sqlalchemy.sql.functions import mode
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import Optional, List


router = APIRouter(
    prefix = "/posts", # This will prefix each request with the specified value
    tags = ["Posts"] # This will create a tag on the documentation
)

###################################################################################
# FUNCTION NAME: GET_POSTS
# THIS FUNCTION WILL RETURN ALL THE POSTS FROM DATABASE
# WE NEED TO USE LIST WHILE DEFINING RESPONSE_MODEL. REASON IS THAT WITHOUT LIST
# IT WILL TRY TO RETURN A LIST BUT WE HAVE DEFINED A SINGLE ITME IN RESPOSE
# MODEL. SO WE HAVE USED LIST[SCHEMAS.POSTRESPONSE]
###################################################################################

# @router.get("/", response_model = List[schemas.PostResponse])
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 2,
                skip: int = 0, search: Optional[str] = ""):

    # We are passing three query parameters:
    # limit: This will limit the number of post returned back to User
    # skip: This will skip these many posts
    # search: This will search the posts as per the given words. Put '%20' for providing space between words

    # cursor.execute("select * from posts")
    # posts = cursor.fetchall()

    # Run Below Query if need to get all post only for the current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    
    # Run Below Query if need to fetch all the posts from database table
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

###################################################################################
# FUNCTION NAME: GET_SINGLE_POST
# THIS FUNCTION WILL RETURN SINGLE POST FROM DATABASE AS PER THE ID PROVIDED
###################################################################################

# @router.get("/{id}", response_model = schemas.PostResponse)
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts where id = %s", (str(id),))
    # post = cursor.fetchone()
    # post = find_post(id)
    # find_post = db.query(models.Post).filter(models.Post.id == id).first()

    find_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not find_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"post with id: {2} was not found"}

    # Put below check to implement the functionality where the user can get the post created by the user
    # if find_post.owner_id != current_user.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    return find_post

    
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     """This func will take Body from input message, convert this to dictionay and save to payLoad variable"""
#     print(payLoad)
#     return{"new message is": f"title: {payLoad['title']} and content is: {payLoad['content']}"}

###################################################################################
# FUNCTION NAME: CREATE_POSTS
# THIS FUNCTION WILL CREATE A POST IN DATABASE
# BEFORE UPDATING THE POST, USER NEEDS TO LOGIN AND TAKE A TOKEN
# THEN WHILE CREATING THE POST, USER NEEDS TO PROVIDE THE TOKEN IN THE HEADER
# OF THE API, AS THERE IS A DEPENDENCY ON "Depends(oauth2.get_current_user)"
###################################################################################

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ This function will take the input data and will check the schema as per Post Class"""
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(f"User Id is: {current_user.id}")

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

###################################################################################
# FUNCTION NAME: DELETE_POST
# THIS FUNCTION WILL DELETE A POST FROM DATABASE
###################################################################################

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # del_post = cursor.fetchone()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id) # It is a query to the database
    post_delete = post_query.first()

    if post_delete == None: # This will use the query and fetch the first matching entry
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    # my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

###################################################################################
# FUNCTION NAME: UPDATE_POST
# THIS FUNCTION WILL UPDATE A POST IN DATABASE
###################################################################################
@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # update = modify_post(id, post)
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_update = post_query.first()

    if post_update == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")

    if post_update.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # conn.commit()
    return post_query.first()

