from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import engine, get_db
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    tags = ["Authentication"]
)

###################################################################################
# FUNCTION NAME: USER_LOGIN
# THIS FUNCTION WILL VERIFY THE PASSWORD OF USER IN USERS TABLE IN FASTAPI DATABASE
###################################################################################
@router.post("/login", response_model=schemas.Token)
def user_login(login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Instead of fetching the users's emailid and password in plain text, we need to use the 
    # OAuthPasswordRequestForm, and it will return:
    # username
    # password

    user_details = db.query(models.User).filter(models.User.email == login_details.username).first()

    if not user_details:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    if not utils.verify_password(login_details.password, user_details.password):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    # create a token
    # return token

    access_token = oauth2.create_access_token(data = {"user_id": user_details.id})

    return {"access_token": access_token, "token_type": "bearer"}

