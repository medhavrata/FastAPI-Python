from sqlalchemy.sql.expression import delete
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix = "/vote", # This will prefix each request with the specified value
    tags = ["Votes"] # This will create a tag on the documentation
)

###################################################################################
# FUNCTION NAME: CREATE_VOTE
# THIS FUNCTION WILL CREATE A VOTE IN VOTES TABLE IN FASTAPI DATABASE
###################################################################################
@router.post("/", status_code = status.HTTP_201_CREATED)
def create_vote(vote : schemas.VoteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ This function will take the input data and will check the schema as per Vote Class"""

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()

    if (vote.post_direction == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully created the vote"}

    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully reset the vote"}